# SPEC.md

## Main flow

1. Waiter logs in.
2. Waiter selects a table.
3. Waiter records a voice command.
4. System transcribes audio.
5. System parses text into structured order actions.
6. Waiter reviews interpreted items/actions.
7. Waiter confirms or edits.
8. System sends confirmed order to kitchen/bar in real time.
9. Kitchen/bar updates item status.
10. Waiter can view table history and close the order.

## Example

Input: Mesa 12, duas picanhas ao ponto, uma Coca Zero e uma água sem gás.

Expected structured output:
- table: 12
- items:
  - Picanha ao ponto, quantity 2
  - Coca Zero, quantity 1
  - Água sem gás, quantity 1

## Supported voice actions

- Add item.
- Change item quantity.
- Remove item.
- Cancel item.
- Close table/order.

## Acceptance criteria

- No order is submitted before confirmation.
- Invalid or ambiguous parsing requires user review.
- Kitchen/bar screen receives confirmed orders in real time.
- Admin can manage users, tables and products.
