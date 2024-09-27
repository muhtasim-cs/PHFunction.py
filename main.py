def findPokerHand(hand):
    """
    Determines the highest poker hand ranking from a list of 5 cards.

    Args:
        hand (list): A list of 5 strings representing the cards, e.g., ["KH", "AH", "QH", "JH", "10H"].

    Returns:
        str: The name of the highest poker hand ranking.
    """
    ranks = []
    suits = []
    possibleRanks = []

    # Mapping of face cards to their corresponding numerical values
    face_card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11}

    # Parse each card to extract rank and suit
    for card in hand:
        # Determine if the card has a single or double character rank
        if len(card) == 2:
            rank_str, suit = card[0], card[1]
        else:
            rank_str, suit = card[:2], card[2]

        # Convert face cards to their numerical values
        rank = face_card_values.get(rank_str, None)
        if rank is None:
            try:
                rank = int(rank_str)
            except ValueError:
                raise ValueError(f"Invalid rank '{rank_str}' in card '{card}'.")

        ranks.append(rank)
        suits.append(suit)

    # Sort the ranks to simplify hand evaluation
    sortedRanks = sorted(ranks)
    handUniqueVals = list(set(sortedRanks))

    # Helper function to check for consecutive ranks (Straight)
    def is_consecutive(sorted_list):
        return all(sorted_list[i] == sorted_list[i - 1] + 1 for i in range(1, len(sorted_list)))

    # Check for Flush (all suits are the same)
    is_flush = suits.count(suits[0]) == 5

    # Check for Straight (all ranks are consecutive)
    is_straight = is_consecutive(sortedRanks)

    # Evaluate special case: Ace-low Straight (A-2-3-4-5)
    if sortedRanks == [2, 3, 4, 5, 14]:
        is_straight = True
        sortedRanks = [1, 2, 3, 4, 5]  # Adjust ranks for Ace-low Straight

    # Determine the highest possible rank based on hand characteristics
    if is_flush and sortedRanks == [10, 11, 12, 13, 14]:
        possibleRanks.append(10)  # Royal Flush
    elif is_flush and is_straight:
        possibleRanks.append(9)   # Straight Flush
    elif is_flush:
        possibleRanks.append(6)   # Flush
    elif is_straight:
        possibleRanks.append(5)   # Straight

    # Count occurrences of each rank to identify multiples
    rank_counts = {rank: sortedRanks.count(rank) for rank in handUniqueVals}

    if len(handUniqueVals) == 2:
        # Either Four of a Kind or Full House
        if 4 in rank_counts.values():
            possibleRanks.append(8)  # Four of a Kind
        if 3 in rank_counts.values():
            possibleRanks.append(7)  # Full House
    elif len(handUniqueVals) == 3:
        # Either Three of a Kind or Two Pair
        if 3 in rank_counts.values():
            possibleRanks.append(4)  # Three of a Kind
        if list(rank_counts.values()).count(2) == 2:
            possibleRanks.append(3)  # Two Pair
    elif len(handUniqueVals) == 4:
        # One Pair
        possibleRanks.append(2)      # Pair

    # If no other hand is identified, it's a High Card
    if not possibleRanks:
        possibleRanks.append(1)      # High Card

    # Mapping of rank values to their corresponding hand names
    pokerHandRanks = {
        10: "Royal Flush",
        9: "Straight Flush",
        8: "Four of a Kind",
        7: "Full House",
        6: "Flush",
        5: "Straight",
        4: "Three of a Kind",
        3: "Two Pair",
        2: "Pair",
        1: "High Card"
    }

    # Determine the highest possible hand from the possible ranks
    highest_rank = max(possibleRanks)
    output = pokerHandRanks[highest_rank]
    print(f"Hand: {hand} --> {output}")
    return output


if __name__ == "__main__":
    # Test cases to validate the function
    test_hands = [
        (["KH", "AH", "QH", "JH", "10H"], "Royal Flush"),
        (["QC", "JC", "10C", "9C", "8C"], "Straight Flush"),
        (["5C", "5S", "5H", "5D", "QH"], "Four of a Kind"),
        (["2H", "2D", "2S", "10H", "10C"], "Full House"),
        (["2D", "KD", "7D", "6D", "5D"], "Flush"),
        (["JC", "10H", "9C", "8C", "7D"], "Straight"),
        (["10H", "10C", "10D", "2D", "5S"], "Three of a Kind"),
        (["KD", "KH", "5C", "5S", "6D"], "Two Pair"),
        (["2D", "2S", "9C", "KD", "10C"], "Pair"),
        (["KD", "5H", "2D", "10C", "JH"], "High Card"),
        (["AD", "2S", "3H", "4C", "5D"], "Straight"),  # Ace-low Straight
        (["AH", "2H", "3H", "4H", "5H"], "Straight Flush")  # Ace-low Straight Flush
    ]

    for hand, expected in test_hands:
        result = findPokerHand(hand)
        assert result == expected, f"Test failed for hand {hand}. Expected: {expected}, Got: {result}"
    print("All tests passed.")

