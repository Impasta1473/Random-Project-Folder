import random
import sys
import time
from collections import deque
DUAL_CARDS = [
	"Mouse", "Keyboard", "Monitor", "Microphone",
	"Speaker"
]
ALL_CARDS = DUAL_CARDS + [
	"Skip", "Transfer", "Randomize", "Inspect Element",
	"Backburn Draw", "Code Patch", "Cyberhack", "NOPE", "Polymorphic Virus",
	"Hack", "Backdoor Transfer", "Disable"
]
class Player:
	def __init__(self, name, is_human=False):
		self.name = name
		self.hand = []
		self.alive = True
		self.is_human = is_human
		self.pending_draws = 1
		self.controlled_turns = 0
		self.controlled_by = None
		self.disabled_turns = 0
	def inspect_element(self, deck):
		if self.is_human:
			print(f"You use inspect element and see the future: {list(deck)[:3]}")
def get_next_player(players, current):
	idx = players.index(current)
	total = len(players)
	for offset in range(1, total):
		next_p = players[(idx + offset) % total]
		if next_p.alive:
			return next_p
	return None
def ask_pvirus(player):
	for p in players:
		if p != player and "Polymorphic Virus" in p.hand:
			if p.is_human:
				choice = input(f"{p.name}, use Polymorphic Virus on {player.name}? (y/n): ")
				if choice.lower() == 'y':
					p.hand.remove("Polymorphic Virus")
					return True
			else:
				if random.random() < 0.5:
					p.hand.remove("Polymorphic Virus")
					return True
	return False
def generate_deck(num_players):
	deck = []
	for _ in range(6):
		deck.append("Skip")
	for _ in range(6):
		deck.append("Transfer")
	for _ in range(6):
		deck.append("Randomize")
	for _ in range(5):
		deck.append("Inspect Element")
	for _ in range(7):
		deck.append("Backburn Draw")
	for _ in range(5):
		deck.append("NOPE")
	for _ in range(2):
		deck.append("Polymorphic Virus")
	for _ in range(5):
		deck.append("Backdoor Transfer")
	for _ in range(5):
		deck.append("Hack")
	for _ in range(4):
		deck.append("Disable")
	for _ in range(4):
		deck.append("Code Patch")
	for _ in range(5):
		deck.extend(DUAL_CARDS)
	random.shuffle(deck)
	return deque(deck)
def draw_card(player, deck, nope_stack):
	global played
	if len(deck) < 3:
		print("Deck low, restocking...")
		for c in played:
			deck += played.pop()
			time.sleep(0.06)
		print("Deck restocked.")
	card = deck.pop()
	played += card
	print(f"{player.name} draws a card")
	time.sleep(1)
	if card == "Cyberattack":
		time.sleep(1.5)
		if "Code Patch" in player.hand:
			print(f"{player.name} has a Code Patch!")
			if ask_pvirus(player):
				if player.hand.count("Code Patch") >= 2:
					player.hand.remove("Code Patch")
					player.hand.remove("Code Patch")
					print(f"{player.name} uses second Code Patch to counter Polymorphic Virus!")
					time.sleep(1)
				else:
					print(f"{player.name}'s computer died due to Polymorphic Virus!")
					time.sleep(1)
					player.alive = False
					if player.is_human:
						sys.exit("Your computer died.")
					return
			else:
				player.hand.remove("Code Patch")
		insert_pos = random.randint(0, len(deck))
		if player.is_human:
			insert_pos = int(input(f"Where do you want to reinsert the Cyberattack? Enter a number between 0 (TOP) and {len(deck)} (BOTTOM)"))
			deck.insert(insert_pos, "Cyberattack")
			print(f"{player.name} used Code Path!")
			time.sleep(1)
		else:
			print(f"{player.name}'s computer died!")
			time.sleep(1)
			player.alive = False
			if player.is_human:
				sys.exit("Your computer died.")
	else:
		player.hand.append(card)
def play_card(player, card_idx, deck, players, current_idx, nope_stack):
	if card_idx < 0 or card_idx >= len(player.hand):
		print("Invalid index.")
		return False
	card = player.hand[card_idx]
	hand = player.hand
	def ask_nope(action_name):
		nonlocal nope_stack
		for p in players:
			if p != player and p.alive and "NOPE" in p.hand:
				if p.is_human:
					ans = input(
						f"{p.name}, do you want to NOPE the action '{action_name}'? (y/n): "
					)
					if ans.lower() == 'y':
						p.hand.remove("NOPE")
						nope_stack.append("NOPE")
						print(f"{p.name} played NOPE!")
						if len(nope_stack) % 2 == 1:
						    return True
				else:
					time.sleep(1)
					if random.random() < 0.4:
						p.hand.remove("NOPE")
						nope_stack.append("NOPE")
						print(f"{p.name} played NOPE!")
						if len(nope_stack) % 2 == 1:
							return True
		return False
	if card == "Code Patch" or card == "Cyberattack" or card == "NOPE" or card == "Polymorphic Virus":
		print("This card cannot be played manually.")
		time.sleep(1)
		return False
	if card == "Skip":
		if ask_nope("Skip"):
			hand.pop(card_idx)
			return False
		else:
			player.pending_draws = 0
			print(f"{player.name} skipped their draw.")
			time.sleep(1)
	elif card == "Transfer":
		if ask_nope("Transfer"):
			hand.pop(card_idx)
			return False
		else:
			next_p = get_next_player(players, player)
			if next_p:
				next_p.pending_draws += 1
				print(f"{player.name} has transferred! {next_p.name} must draw twice.")
				time.sleep(1)
			player.pending_draws = 0
	elif card == "Randomize":
		if ask_nope("Randomize"):
			hand.pop(card_idx)
			return False
		else:
			random.shuffle(deck)
			print("Deck randomized.")
			time.sleep(1)
	elif card == "Inspect Element":
		if ask_nope("Inspect Element"):
			hand.pop(card_idx)
			return False
		else:
			player.inspect_element(deck)
	elif card == "Backburn Draw":
		if ask_nope("Backburn Draw"):
			hand.pop(card_idx)
			return False
		else:
			card_drawn = deck.popleft()
			if player.is_human:
				print(f"{player.name} drew from bottom: {card_drawn}")
			time.sleep(1)
			if card_drawn == "Cyberattack":
				if "Code Patch" in hand:
					print(f"{player.name} used Code Patch!")
					time.sleep(1)
					if ask_pvirus(player):
						if hand.count("Code Patch") >= 2:
							hand.remove("Code Patch")
							hand.remove("Code Patch")
							print(f"{player.name} uses second Code Patch to counter Polymorphic Virus!")
							time.sleep(1)
						else:
							print(f"{player.name}'s computer died due to Polymorphic Virus!")
							time.sleep(1)
							player.alive = False
							if player.is_human:
								sys.exit("Your computer died.")
							return True
					else:
						hand.remove("Code Patch")
						insert_pos = random.randint(0, len(deck))
						deck.insert(insert_pos, "Cyberattack")
				else:
					print(f"{player.name}'s computer died!")
					time.sleep(1)
					player.alive = False
					if player.is_human:
						sys.exit("Your computer died.")
					return True
			else:
				hand.append(card_drawn)
	elif card in DUAL_CARDS:
		if hand.count(card) >= 2:
			if ask_nope("Card Combo"):
				hand.pop(card_idx)
				return False
			else:
				target = get_next_player(players, player)
				if target and target.hand:
					stolen = random.choice(target.hand)
					target.hand.remove(stolen)
					hand.append(stolen)
					if player.is_human:
						print(f"{player.name} stole {stolen} from {target.name}!")	
					time.sleep(1)
					hand.remove(card)
					hand.remove(card)
					return True
				else:
					print("No valid target.")
					time.sleep(1)
					return False
		else:
			print("You need two of the same dual card to steal.")
			time.sleep(1)
			return False
	elif card == "Backdoor Transfer":
		if ask_nope("Backdoor Transfer"):
			hand.pop(card_idx)
			return False
		else:
			for p in players:
				if p != player and p.alive:
					given = []
					for _ in range(2):
						if p.hand:
							given.append(p.hand.pop(0))
					hand.extend(given)
					print(f"{p.name} gave {given} to {player.name}.")
					time.sleep(1)
	elif card == "Hack":
		if ask_nope("Hack"):
			hand.pop(card_idx)
			return False
		next_p = get_next_player(players, player)
		if next_p:
			next_p.controlled_turns = 2
			next_p.controlled_by = player
			print(f"{player.name} will control {next_p.name}'s next 2 turns.")
			time.sleep(1)
	elif card == "Disable":
		if ask_nope("Disable"):
			hand.pop(card_idx)
			return False
		next_p = get_next_player(players, player)
		if next_p:
			next_p.disabled_turns = 2
			print(f"{next_p.name} is disabled for 2 turns.")
			time.sleep(1)
	else:
		print("Unrecognized card.")
		time.sleep(1)
		return False
	hand.pop(card_idx)
	return True
altering = False
players = []
played = []
num_ai = int(input("Enter number of AI players: "))
while num_ai < 1 or num_ai > 6:
	print("Please choose a number between 1 and 5.")
	num_ai = int(input("Enter number of AI players: "))
p_name = input("Enter your name: ")
players = [Player(p_name, is_human=True)] + [Player(f"Player {i+2}") for i in range(num_ai)]
deck = generate_deck(len(players))
for player in players:
	for _ in range(5):
		player.hand.append(deck.pop())
	player.hand.append("Code Patch")

for _ in range(len(players) - 1):
	deck.append("Cyberattack")
random.shuffle(deck)
current_idx = 0
nope_stack = []
while True:
	player = players[current_idx]
	if not player.alive:
		current_idx = (current_idx + 1) % len(players)
		continue
	controller = player
	if player.controlled_turns > 0 and player.controlled_by:
		controller = player.controlled_by
		player.controlled_turns -= 1
	if player.disabled_turns > 0:
		print(f"{player.name} is disable and skips turn.")
		time.sleep(1)
		player.disabled_turns -= 1
		current_idx = (current_idx + 1) % len(players)
		continue
	print(f"\n{player.name}'s turn:")
	time.sleep(1)
	if controller.is_human:
		while True:
			print(player.name + f"'s hand: {[f'{i}: {card}' for i, card in enumerate(player.hand)]}")
			choice = input("Enter card index to play or press Enter to draw: ")
			if choice == "":
				break
			try:
				card_idx = int(choice)
				if play_card(player,  card_idx, deck, players, current_idx, nope_stack):
					break
			except:
				print("Invalid input.")
				time.sleep(1)
	else:
		playable = [
			i for i, c in enumerate(player.hand)
			if c not in ["Code Patch", "Cyberattack"]
		]
		if playable and random.random() < 0.8:
			play_card(player, random.choice(playable), deck, players,
					  current_idx, nope_stack)
	while player.pending_draws > 0:
		draw_card(player, deck, nope_stack)
		if not player.alive:
			break
		player.pending_draws -= 1
	player.pending_draws = 1
	current_idx = (current_idx + 1) % len(players)
	alive_players = [p for p in players if p.alive]
	if len(alive_players) == 1:
		print(f"\n{alive_players[0].name} wins!")
		time.sleep(1)
		break
main()
