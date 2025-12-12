# final_reservation_hyd_to_london.py
# Single-flight reservation (fixed route Hyderabad -> London, time 6:00 PM)
# Supports: Add (reserve), Cancel by ID, Check by name, List, View flight info, Tests, Exit

class Passenger:
    def __init__(self, rid, name, seat, food):
        self.id = rid
        self.name = name
        self.seat = seat
        self.food = food
        self.next = None

class Flight:
    def __init__(self):
        self.head = None
        self._next_id = 1
        self.taken_seats = set()
        self.flight_time = "6:00 PM"        # fixed
        self.start = "Hyderabad"            # fixed
        self.dest = "London"                # fixed
        self.food_options = ["Veg", "Non-Veg", "No Meal"]

    def reserve(self, name, seat, food_idx):
        name = (name or "").strip()
        seat = (seat or "").strip().upper()
        if not name:
            return None, "Invalid name"
        if not seat:
            return None, "Invalid seat"
        if seat in self.taken_seats:
            return None, "Seat already taken"
        if not isinstance(food_idx, int) or not (0 <= food_idx < len(self.food_options)):
            return None, "Invalid food choice"

        rid = self._next_id
        self._next_id += 1
        node = Passenger(rid, name, seat, self.food_options[food_idx])
        self.taken_seats.add(seat)

        # Insert alphabetically by name; stable by id for same names
        if not self.head or name < self.head.name:
            node.next = self.head
            self.head = node
            return rid, "Reserved"
        prev, cur = self.head, self.head.next
        while cur and (cur.name < name or (cur.name == name and cur.id < node.id)):
            prev, cur = cur, cur.next
        prev.next = node
        node.next = cur
        return rid, "Reserved"

    def cancel_by_id(self, rid):
        if not self.head:
            return False
        if self.head.id == rid:
            self.taken_seats.discard(self.head.seat)
            self.head = self.head.next
            return True
        prev, cur = self.head, self.head.next
        while cur and cur.id != rid:
            prev, cur = cur, cur.next
        if not cur:
            return False
        self.taken_seats.discard(cur.seat)
        prev.next = cur.next
        return True

    def check_by_name(self, name):
        name = (name or "").strip()
        cur = self.head
        res = []
        while cur:
            if cur.name == name:
                res.append((cur.id, cur.seat, cur.food))
            cur = cur.next
        return res

    def list_passengers(self):
        cur = self.head
        out = []
        while cur:
            out.append((cur.id, cur.name, cur.seat, cur.food))
            cur = cur.next
        return out

def run_quick_tests():
    f = Flight()
    id1, _ = f.reserve("Ravi", "1A", 0)
    id2, _ = f.reserve("Ravi", "1B", 1)
    id3, _ = f.reserve("Anu", "2A", 0)
    assert id1 and id2 and id3
    assert f.check_by_name("Ravi") == [(id1,"1A","Veg"), (id2,"1B","Non-Veg")]
    assert not f.reserve("X", "1A", 0)[0]  # seat taken
    assert f.cancel_by_id(id1)
    assert f.check_by_name("Ravi") == [(id2,"1B","Non-Veg")]
    print("Quick tests passed.")

def main():
    f = Flight()
    menu_line = "1 Add  |  2 Cancel  |  3 Check  |  4 List  |  5 FlightInfo  |  6 Tests  |  7 Exit"
    print("\n" + menu_line + "\n")

    while True:
        choice = input("Choice (1-7): ").strip()
        if choice == "1":
            name = input("Name: ").strip()
            seat = input("Seat (e.g., 1A): ").strip()
            print("Food options: 0 Veg  /  1 Non-Veg  /  2 No Meal")
            idx = input("Food index: ").strip()
            if not idx.isdigit():
                print("Invalid food index"); continue
            rid, msg = f.reserve(name, seat, int(idx))
            if rid:
                print(f"Reserved. ID={rid}")
            else:
                print("Failed to reserve:", msg)
        elif choice == "2":
            sid = input("Reservation ID to cancel: ").strip()
            if not sid.isdigit():
                print("Enter numeric ID"); continue
            print("Cancelled" if f.cancel_by_id(int(sid)) else "ID not found")
        elif choice == "3":
            name = input("Name to check: ").strip()
            res = f.check_by_name(name)
            if not res:
                print("No reservations with that name")
            else:
                print("Matches:", "  ".join(f"[{rid}] Seat:{seat} Meal:{food}" for rid,seat,food in res))
        elif choice == "4":
            lst = f.list_passengers()
            if not lst:
                print("No passengers")
            else:
                for rid,name,seat,food in lst:
                    print(f"[{rid}] {name} | Seat:{seat} | Meal:{food}")
        elif choice == "5":
            print(f"Flight Time: {f.flight_time}   Start: {f.start}   Destination: {f.dest}")
        elif choice == "6":
            run_quick_tests()
        elif choice == "7":
            print("Exiting..."); break
        else:
            print("Invalid choice (1-7)")

if __name__ == "__main__":
    main()
