### 🏸 *Core Functionalities*

 1.⁠ ⁠*Player Input Options*:
   - Upload player names via *CSV or Excel* (expects a ⁠ Name ⁠ column).
   - Manually enter player names as a *comma-separated list*.

 2.⁠ ⁠*Player Selection*:
   - Select *players present today* from the uploaded or entered list.
   - Dynamically update this list as players are added or removed.

 3.⁠ ⁠*Court Configuration*:
   - Input the *number of available courts* (minimum 1).
   - Courts can host either *doubles (4 players)* or *singles (2 players)* matches.

---

### 🔁 *Rotation Logic*

 4.⁠ ⁠*Minimum Requirements*:
   - Requires at least *3 active players* to begin rotation.
   - Smart allocation of players to courts based on availability.

 5.⁠ ⁠*Smart Match Allocation*:
   - Prioritizes *doubles matches* when enough players are available.
   - Falls back to *singles matches* when fewer players are available.
   - Ensures *no court is left underutilized* if players are sufficient.

 6.⁠ ⁠*Bench Management*:
   - Excess players are *benched* and rotated in future matches.
   - Bench queue is maintained and updated after each rotation.

---

### 🛋️ *Rest/Break Handling*

 7.⁠ ⁠*Voluntary Rest Area*:
   - Players can be moved to a *rest/break list*.
   - These players are *excluded from court allocation*.
   - Once removed from rest, they are *automatically re-included* in the active pool.

 8.⁠ ⁠*Dynamic Active Player Calculation*:
   - Before each rotation, the app *recalculates active players* by excluding those resting.
   - Prevents resting players from being accidentally assigned to courts.

---

### 🧾 *Rotation History Tracking*

 9.⁠ ⁠*Detailed Match History*:
   - Each rotation logs:
     - Court-to-player allocations
     - Benched players
     - Resting players
   - Displayed in a *chronological history section*.

10.⁠ ⁠*Reset Functionality*:
    - A reset button clears:
      - Rotation count
      - Bench queue
      - Resting players
      - Rotation history

