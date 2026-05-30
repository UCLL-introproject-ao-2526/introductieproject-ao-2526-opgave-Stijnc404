import copy
import random
import pygame

pygame.init()
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
#win, loss, draw/push
record = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'PLAYER BUSTED o_0', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
animations = []
countdown = 10
countdown_timer = 0
max_score = 21

class CardAnimation:
    def __init__(self, card, start_x, start_y, end_x, end_y, target_hand, card_index):
        self.card = card
        self.x = float(start_x)
        self.y = float(start_y)
        self.end_x = float(end_x)
        self.end_y = float(end_y)
        self.target_hand = target_hand
        self.card_index = card_index
        self.done = False

    def update(self):
        dx = self.end_x - self.x
        dy = self.end_y - self.y
        self.x += dx * 0.2
        self.y += dy * 0.2
        if abs(dx) < 1 and abs(dy) < 1:
            self.x = self.end_x
            self.y = self.end_y
            self.done = True

    def draw(self, screen, font):
        color = (70, 130, 180) if self.target_hand == 'player' else (180, 60, 60)
        pygame.draw.rect(screen, color, [self.x, self.y, 120, 220], 0, 8)
        pygame.draw.rect(screen, 'white', [self.x + 8, self.y + 8, 104, 204], 0, 6)
        screen.blit(font.render(self.card, True, 'black'), (self.x + 14, self.y + 14))
        screen.blit(font.render(self.card, True, 'black'), (self.x + 14, self.y + 175))
        pygame.draw.rect(screen, 'black', [self.x, self.y, 120, 220], 3, 8)

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, currennt_deck, target='player'):
    card = random.randint(0, len(currennt_deck) - 1)
    drawn_card = currennt_deck[card]
    currennt_deck.pop(card)
    i = len(current_hand)
    if target == 'player':
        end_x = 70 + (70 * i)
        end_y = 460 + (5 * i)
        animations.append(CardAnimation(drawn_card, end_x, HEIGHT + 50, end_x, end_y, 'player', i))
    else:
        end_x = 70 + (70 * i)
        end_y = 160 + (5 * i)
        animations.append(CardAnimation(drawn_card, end_x, -280, end_x, end_y, 'dealer', i))
    current_hand.append(drawn_card)
    return current_hand, currennt_deck

# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

# draw cards visualy onto the screen
def draw_cards(player, dealer, reveal, skip_player=[], skip_dealer=[], result=0):
    for i in range(len(player)):
        if i in skip_player:
            continue
        x = 70 + (70 * i)
        y = 460 + (5 * i)
        pygame.draw.rect(screen, (70, 130, 180), [x, y, 120, 220], 0, 8)
        pygame.draw.rect(screen, 'white', [x + 8, y + 8, 104, 204], 0, 6)
        screen.blit(font.render(player[i], True, 'black'), (x + 14, y + 14))
        screen.blit(font.render(player[i], True, 'black'), (x + 14, y + 175))
        pygame.draw.rect(screen, 'black', [x, y, 120, 220], 3, 8)
    if result in [1, 3] and len(player) > 0:
        x1 = 70
        y1 = 460
        x2 = 70 + (70 * (len(player) - 1)) + 120
        y2 = 460 + (5 * (len(player) - 1)) + 220
        pygame.draw.line(screen, 'white', (x1, y1), (x2, y2), 4)
        pygame.draw.line(screen, 'white', (x2, y1), (x1, y2), 4)

    for i in range(len(dealer)):
        if i in skip_dealer:
            continue
        x = 70 + (70 * i)
        y = 160 + (5 * i)
        pygame.draw.rect(screen, (180, 60, 60), [x, y, 120, 220], 0, 8)
        pygame.draw.rect(screen, 'white', [x + 8, y + 8, 104, 204], 0, 6)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (x + 14, y + 14))
            screen.blit(font.render(dealer[i], True, 'black'), (x + 14, y + 175))
        else:
            screen.blit(font.render('???', True, 'black'), (x + 14, y + 14))
            screen.blit(font.render('???', True, 'black'), (x + 14, y + 175))
        pygame.draw.rect(screen, 'black', [x, y, 120, 220], 3, 8)
    if result == 2 and len(dealer) > 0:
        x1 = 70
        y1 = 160
        x2 = 70 + (70 * (len(dealer) - 1)) + 120
        y2 = 160 + (5 * (len(dealer) - 1)) + 220
        pygame.draw.line(screen, 'white', (x1, y1), (x2, y2), 4)
        pygame.draw.line(screen, 'white', (x2, y1), (x1, y2), 4)

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for card in hand:
        if card.isdigit() and card != 'A':
            hand_score += int(card)
        elif card in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif card == 'A':
            hand_score += 11
    for _ in range(aces_count):
        if hand_score > max_score:
            hand_score -= 10
    return hand_score

# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    pygame.draw.rect(screen, (20, 100, 40), [0, 0, WIDTH, 80])
    pygame.draw.rect(screen, (10, 60, 20), [0, 0, WIDTH, 80], 3)

    if not act:
        deal = pygame.draw.rect(screen, (255, 215, 0), [150, 15, 300, 50], 0, 8)
        pygame.draw.rect(screen, 'black', [150, 15, 300, 50], 3, 8)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 27))
        button_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, (50, 200, 80), [0, 700, 150, 50], 0, 8)
        pygame.draw.rect(screen, 'black', [0, 700, 150, 50], 3, 8)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (15, 712))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, (200, 60, 60), [300, 700, 150, 50], 0, 8)
        pygame.draw.rect(screen, 'black', [300, 700, 150, 50], 3, 8)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (320, 712))
        button_list.append(stand)

        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))

        bar_width = int((countdown / 10) * WIDTH)
        r = int(255 * (1 - countdown / 10))
        g = int(255 * (countdown / 10))
        pygame.draw.rect(screen, (r, g, 0), [0, 760, bar_width, 18], 0, 4)
        pygame.draw.rect(screen, 'white', [0, 760, WIDTH, 18], 2, 4)
        screen.blit(font.render(f'{int(countdown)}s', True, 'white'), (WIDTH - 40, 758))
        screen.blit(font.render(f'Target: {max_score}', True, (255, 215, 0)), (160, 712))

    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal_text = smaller_font.render('NEW HAND', True, (255, 225, 0))
        deal = deal_text.get_rect(center=(300, 800))
        screen.blit(deal_text, deal)
        pygame.draw.line(screen, (255, 215, 0), (deal.left, deal.bottom + 3), (deal.right, deal.bottom + 3), 2)
        button_list.append(deal)
    return button_list

# check endgame conditions function
def check_endgame(hand_act, dealer_score, player_score, result, totals, add):
    if not hand_act and dealer_score >= 17:
        if player_score > max_score:
            result = 1
        elif dealer_score < player_score <= max_score or dealer_score > max_score:
            result = 2
        elif player_score < dealer_score <= max_score:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

#main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill((34, 120, 60))

    if initial_deal:
        max_score = random.choice([21, 21, 21, 23])
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck, 'player')
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck, 'dealer')
        initial_deal = False

    still_animating = False
    for anim in animations[:]:
        anim.update()
        anim.draw(screen, font)
        if anim.done:
            animations.remove(anim)
        else:
            still_animating = True

    if active:
        player_score = calculate_score(my_hand)
        skip_p = [a.card_index for a in animations if a.target_hand == 'player']
        skip_d = [a.card_index for a in animations if a.target_hand == 'dealer']
        draw_cards(my_hand, dealer_hand, reveal_dealer, skip_p, skip_d, outcome)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17 and not still_animating:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck, 'dealer')
        draw_scores(player_score, dealer_score)

        if hand_active and not still_animating:
            countdown_timer += 1
            if countdown_timer >= fps:
                countdown -= 1
                countdown_timer = 0
            if countdown <= 0:
                reveal_dealer = True
                hand_active = False

    buttons = draw_game(active, record, outcome)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    animations = []
                    countdown = 10
                    countdown_timer = 0

            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < max_score and hand_active and not still_animating:
                    my_hand, game_deck = deal_cards(my_hand, game_deck, 'player')
                    countdown = 10
                    countdown_timer = 0

                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer and not still_animating:
                    reveal_dealer = True
                    hand_active = False

                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        reveal_dealer = False
                        outcome = 0
                        hand_active = True
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        animations = []
                        countdown = 10
                        countdown_timer = 0

    # if player busts or reaches target, automatically end turn
    if hand_active and player_score >= max_score:
        hand_active = False
        reveal_dealer = True

    outcome, record, add_score = check_endgame(
        hand_active,
        dealer_score,
        player_score,
        outcome,
        record,
        add_score
    )
    pygame.display.flip()
pygame.quit()