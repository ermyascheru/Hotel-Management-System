# ============================================
# HOTEL MANAGEMENT SYSTEM
# ============================================

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import uuid


# --------------------------------------------
# ENUMS FOR TYPE SAFETY
# --------------------------------------------
class RoomType(Enum):
    """
    ENUM: Defines fixed room types.
    Better than strings for type safety and auto-completion.
    """
    SINGLE = "Single"
    DOUBLE = "Double"
    SUITE = "Suite"
    DELUXE = "Deluxe"
    PRESIDENTIAL = "Presidential"


class RoomStatus(Enum):
    """Room availability status."""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Under Maintenance"
    RESERVED = "Reserved"
    CLEANING = "Cleaning"


class ReservationStatus(Enum):
    """Reservation lifecycle status."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    CHECKED_OUT = "Checked Out"
    CANCELLED = "Cancelled"


class PaymentMethod(Enum):
    """Accepted payment methods."""
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    BANK_TRANSFER = "Bank Transfer"


class PaymentStatus(Enum):
    """Payment status tracking."""
    PENDING = "Pending"
    PARTIAL = "Partially Paid"
    COMPLETED = "Completed"
    REFUNDED = "Refunded"


# --------------------------------------------
# ROOM CLASS
# --------------------------------------------
class Room:
    """
    Represents a hotel room.
    
    Each room has a type, price, amenities, and status.
    """
    
    # Class variable: base prices per room type
    BASE_PRICES = {
        RoomType.SINGLE: 80,
        RoomType.DOUBLE: 120,
        RoomType.SUITE: 200,
        RoomType.DELUXE: 300,
        RoomType.PRESIDENTIAL: 500
    }
    
    def __init__(self, room_number: str, room_type: RoomType, 
                 floor: int, price_override: Optional[float] = None):
        self._room_number = room_number
        self._room_type = room_type
        self._floor = floor
        self._status = RoomStatus.AVAILABLE
        
        # Allow custom pricing or use base price
        self._price_per_night = price_override or self.BASE_PRICES[room_type]
        
        # Default amenities based on room type
        self._amenities = self._get_default_amenities()
        
        # Maintenance log
        self._maintenance_history: list[dict] = []
    
    def _get_default_amenities(self) -> list[str]:
        """Assign amenities based on room type."""
        base = ["Wi-Fi", "TV", "Air Conditioning", "Mini Fridge"]
        
        if self._room_type == RoomType.SINGLE:
            return base
        elif self._room_type == RoomType.DOUBLE:
            return base + ["Coffee Maker", "Safe"]
        elif self._room_type == RoomType.SUITE:
            return base + ["Coffee Maker", "Safe", "Living Area", "Bathtub"]
        elif self._room_type == RoomType.DELUXE:
            return base + ["Coffee Maker", "Safe", "Living Area", 
                          "Bathtub", "Balcony", "Mini Bar"]
        else:  # Presidential
            return base + ["Coffee Maker", "Safe", "Living Area", 
                          "Jacuzzi", "Balcony", "Full Bar", 
                          "Butler Service", "Private Dining"]
    
    @property
    def room_number(self) -> str:
        return self._room_number
    
    @property
    def room_type(self) -> RoomType:
        return self._room_type
    
    @property
    def status(self) -> RoomStatus:
        return self._status
    
    @property
    def price_per_night(self) -> float:
        return self._price_per_night
    
    @property
    def is_available(self) -> bool:
        return self._status == RoomStatus.AVAILABLE
    
    def set_status(self, status: RoomStatus):
        """Update room status."""
        old_status = self._status
        self._status = status
        print(f"Room {self._room_number}: {old_status.value} → {status.value}")
    
    def add_amenity(self, amenity: str):
        """Add an amenity to the room."""
        if amenity not in self._amenities:
            self._amenities.append(amenity)
    
    def schedule_maintenance(self, issue: str, scheduled_date: datetime):
        """Schedule maintenance for the room."""
        self._maintenance_history.append({
            "issue": issue,
            "scheduled_date": scheduled_date,
            "completed": False
        })
        self._status = RoomStatus.MAINTENANCE
    
    def complete_maintenance(self):
        """Mark current maintenance as complete."""
        for record in self._maintenance_history:
            if not record["completed"]:
                record["completed"] = True
                record["completed_date"] = datetime.now()
        self._status = RoomStatus.AVAILABLE
    
    def get_info(self) -> dict:
        return {
            "room_number": self._room_number,
            "type": self._room_type.value,
            "floor": self._floor,
            "status": self._status.value,
            "price_per_night": f"${self._price_per_night:.2f}",
            "amenities": self._amenities
        }
    
    def __str__(self):
        return f"Room {self._room_number} ({self._room_type.value})"
    
    def __repr__(self):
        return f"Room({self._room_number}, {self._room_type.value}, {self._status.value})"


# --------------------------------------------
# GUEST CLASS
# --------------------------------------------
class Guest:
    """
    Represents a hotel guest.
    
    Tracks personal info, stay history, and loyalty points.
    """
    
    def __init__(self, guest_id: str, name: str, email: str, 
                 phone: str, id_type: str, id_number: str):
        self._guest_id = guest_id
        self._name = name
        self._email = email
        self._phone = phone
        self._id_type = id_type  # passport, driver's license, etc.
        self._id_number = id_number
        
        self._address: Optional[str] = None
        self._loyalty_points = 0
        self._vip_status = False
        self._stay_history: list['Reservation'] = []
        self._preferences: dict = {}
        self._created_at = datetime.now()
    
    @property
    def guest_id(self) -> str:
        return self._guest_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def loyalty_points(self) -> int:
        return self._loyalty_points
    
    @property
    def is_vip(self) -> bool:
        return self._vip_status or self._loyalty_points >= 10000
    
    def add_loyalty_points(self, points: int):
        """Add loyalty points (earned from stays and spending)."""
        self._loyalty_points += points
        
        # Auto-upgrade to VIP at 10000 points
        if self._loyalty_points >= 10000 and not self._vip_status:
            self._vip_status = True
            print(f"🌟 {self._name} has been upgraded to VIP status!")
    
    def redeem_points(self, points: int) -> bool:
        """Redeem loyalty points for discounts."""
        if points > self._loyalty_points:
            print(f"Insufficient points. Available: {self._loyalty_points}")
            return False
        
        self._loyalty_points -= points
        return True
    
    def set_preference(self, key: str, value: str):
        """Store guest preferences (room temp, pillow type, etc.)."""
        self._preferences[key] = value
    
    def add_to_history(self, reservation: 'Reservation'):
        """Add a reservation to stay history."""
        self._stay_history.append(reservation)
    
    def get_stay_count(self) -> int:
        """Get total number of completed stays."""
        return len([r for r in self._stay_history 
                   if r.status == ReservationStatus.CHECKED_OUT])
    
    def get_info(self) -> dict:
        return {
            "guest_id": self._guest_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "loyalty_points": self._loyalty_points,
            "vip_status": "VIP" if self.is_vip else "Regular",
            "total_stays": self.get_stay_count(),
            "preferences": self._preferences
        }
    
    def __str__(self):
        status = "VIP" if self.is_vip else "Guest"
        return f"{self._name} ({status})"


# --------------------------------------------
# SERVICE CLASS
# --------------------------------------------
class Service:
    """
    Represents additional hotel services.
    
    Examples: room service, spa, laundry, etc.
    """
    
    def __init__(self, service_id: str, name: str, 
                 description: str, price: float):
        self._service_id = service_id
        self._name = name
        self._description = description
        self._price = price
        self._active = True
    
    @property
    def service_id(self) -> str:
        return self._service_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def price(self) -> float:
        return self._price
    
    def get_info(self) -> dict:
        return {
            "service_id": self._service_id,
            "name": self._name,
            "description": self._description,
            "price": f"${self._price:.2f}"
        }


# --------------------------------------------
# BILL CLASS
# --------------------------------------------
class Bill:
    """
    Tracks all charges for a reservation.
    
    AGGREGATION: Contains line items (charges) that can exist
    independently but are grouped together.
    """
    
    def __init__(self, bill_id: str, reservation: 'Reservation'):
        self._bill_id = bill_id
        self._reservation = reservation
        self._line_items: list[dict] = []
        self._payments: list[dict] = []
        self._payment_status = PaymentStatus.PENDING
        self._created_at = datetime.now()
        
        # Automatically add room charge
        self._add_room_charges()
    
    def _add_room_charges(self):
        """Calculate and add room charges based on stay duration."""
        nights = self._reservation.get_nights()
        room_rate = self._reservation.room.price_per_night
        
        # VIP discount
        discount = 0.1 if self._reservation.guest.is_vip else 0
        discounted_rate = room_rate * (1 - discount)
        
        self._line_items.append({
            "description": f"Room {self._reservation.room.room_number} - "
                          f"{nights} night(s) @ ${discounted_rate:.2f}",
            "quantity": nights,
            "unit_price": discounted_rate,
            "total": nights * discounted_rate,
            "category": "Room",
            "date": datetime.now()
        })
    
    def add_service_charge(self, service: Service, quantity: int = 1):
        """Add a service charge to the bill."""
        self._line_items.append({
            "description": service.name,
            "quantity": quantity,
            "unit_price": service.price,
            "total": service.price * quantity,
            "category": "Service",
            "date": datetime.now()
        })
        print(f"✓ Added {service.name} x{quantity} to bill")
    
    def add_custom_charge(self, description: str, amount: float, category: str):
        """Add a custom charge (minibar, damage, etc.)."""
        self._line_items.append({
            "description": description,
            "quantity": 1,
            "unit_price": amount,
            "total": amount,
            "category": category,
            "date": datetime.now()
        })
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal before tax."""
        return sum(item["total"] for item in self._line_items)
    
    def calculate_tax(self, tax_rate: float = 0.12) -> float:
        """Calculate tax amount (default 12%)."""
        return self.calculate_subtotal() * tax_rate
    
    def calculate_total(self, tax_rate: float = 0.12) -> float:
        """Calculate final total with tax."""
        return self.calculate_subtotal() + self.calculate_tax(tax_rate)
    
    def get_amount_paid(self) -> float:
        """Get total amount paid so far."""
        return sum(p["amount"] for p in self._payments)
    
    def get_balance_due(self) -> float:
        """Get remaining balance."""
        return self.calculate_total() - self.get_amount_paid()
    
    def add_payment(self, amount: float, method: PaymentMethod) -> bool:
        """Record a payment."""
        balance = self.get_balance_due()
        
        if amount > balance:
            print(f"Warning: Payment ${amount:.2f} exceeds balance ${balance:.2f}")
            amount = balance  # Cap at balance due
        
        self._payments.append({
            "amount": amount,
            "method": method.value,
            "date": datetime.now(),
            "reference": str(uuid.uuid4())[:8]
        })
        
        # Update payment status
        if self.get_balance_due() <= 0:
            self._payment_status = PaymentStatus.COMPLETED
            print(f"✓ Bill paid in full")
        else:
            self._payment_status = PaymentStatus.PARTIAL
            print(f"✓ Payment of ${amount:.2f} received. Balance: ${self.get_balance_due():.2f}")
        
        return True
    
    def get_summary(self) -> dict:
        """Get complete bill summary."""
        return {
            "bill_id": self._bill_id,
            "guest": self._reservation.guest.name,
            "room": self._reservation.room.room_number,
            "line_items": self._line_items,
            "subtotal": f"${self.calculate_subtotal():.2f}",
            "tax": f"${self.calculate_tax():.2f}",
            "total": f"${self.calculate_total():.2f}",
            "amount_paid": f"${self.get_amount_paid():.2f}",
            "balance_due": f"${self.get_balance_due():.2f}",
            "payment_status": self._payment_status.value,
            "payments": self._payments
        }
    
    def print_invoice(self):
        """Print formatted invoice."""
        print("\n" + "=" * 50)
        print("                    INVOICE")
        print("=" * 50)
        print(f"Bill ID: {self._bill_id}")
        print(f"Date: {self._created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Guest: {self._reservation.guest.name}")
        print(f"Room: {self._reservation.room.room_number}")
        print("-" * 50)
        
        for item in self._line_items:
            print(f"{item['description']}")
            print(f"  {item['quantity']} x ${item['unit_price']:.2f} = ${item['total']:.2f}")
        
        print("-" * 50)
        print(f"Subtotal:     ${self.calculate_subtotal():>10.2f}")
        print(f"Tax (12%):    ${self.calculate_tax():>10.2f}")
        print(f"TOTAL:        ${self.calculate_total():>10.2f}")
        print("-" * 50)
        print(f"Amount Paid:  ${self.get_amount_paid():>10.2f}")
        print(f"Balance Due:  ${self.get_balance_due():>10.2f}")
        print("=" * 50)


# --------------------------------------------
# RESERVATION CLASS
# --------------------------------------------
class Reservation:
    """
    Represents a booking/reservation.
    
    Links Guest, Room, and Bill together.
    Manages the complete reservation lifecycle.
    """
    
    def __init__(self, reservation_id: str, guest: Guest, room: Room,
                 check_in_date: datetime, check_out_date: datetime):
        
        if check_out_date <= check_in_date:
            raise ValueError("Check-out must be after check-in")
        
        self._reservation_id = reservation_id
        self._guest = guest
        self._room = room
        self._check_in_date = check_in_date
        self._check_out_date = check_out_date
        self._status = ReservationStatus.PENDING
        self._bill: Optional[Bill] = None
        self._special_requests: list[str] = []
        self._created_at = datetime.now()
        
        # Actual check-in/out times (vs planned)
        self._actual_check_in: Optional[datetime] = None
        self._actual_check_out: Optional[datetime] = None
    
    @property
    def reservation_id(self) -> str:
        return self._reservation_id
    
    @property
    def guest(self) -> Guest:
        return self._guest
    
    @property
    def room(self) -> Room:
        return self._room
    
    @property
    def status(self) -> ReservationStatus:
        return self._status
    
    @property
    def bill(self) -> Optional[Bill]:
        return self._bill
    
    def get_nights(self) -> int:
        """Calculate number of nights for the stay."""
        delta = self._check_out_date - self._check_in_date
        return delta.days
    
    def add_special_request(self, request: str):
        """Add a special request (late checkout, extra pillows, etc.)."""
        self._special_requests.append(request)
    
    def confirm(self) -> bool:
        """Confirm the reservation."""
        if self._status != ReservationStatus.PENDING:
            print(f"Cannot confirm: current status is {self._status.value}")
            return False
        
        self._status = ReservationStatus.CONFIRMED
        self._room.set_status(RoomStatus.RESERVED)
        print(f"✓ Reservation {self._reservation_id} confirmed")
        return True
    
    def check_in(self) -> bool:
        """Process guest check-in."""
        if self._status not in [ReservationStatus.CONFIRMED, ReservationStatus.PENDING]:
            print(f"Cannot check in: current status is {self._status.value}")
            return False
        
        self._status = ReservationStatus.CHECKED_IN
        self._actual_check_in = datetime.now()
        self._room.set_status(RoomStatus.OCCUPIED)
        
        # Create bill on check-in
        bill_id = f"BILL-{self._reservation_id}"
        self._bill = Bill(bill_id, self)
        
        print(f"✓ {self._guest.name} checked into Room {self._room.room_number}")
        return True
    
    def check_out(self) -> Bill:
        """Process guest check-out."""
        if self._status != ReservationStatus.CHECKED_IN:
            print(f"Cannot check out: current status is {self._status.value}")
            return None
        
        self._status = ReservationStatus.CHECKED_OUT
        self._actual_check_out = datetime.now()
        self._room.set_status(RoomStatus.CLEANING)
        
        # Add loyalty points (10 points per dollar spent)
        total = self._bill.calculate_total()
        points = int(total * 10)
        self._guest.add_loyalty_points(points)
        
        # Add to guest history
        self._guest.add_to_history(self)
        
        print(f"✓ {self._guest.name} checked out. Earned {points} loyalty points!")
        return self._bill
    
    def cancel(self, reason: str = "") -> bool:
        """Cancel the reservation."""
        if self._status in [ReservationStatus.CHECKED_IN, ReservationStatus.CHECKED_OUT]:
            print(f"Cannot cancel: guest has already checked in")
            return False
        
        self._status = ReservationStatus.CANCELLED
        self._room.set_status(RoomStatus.AVAILABLE)
        print(f"✓ Reservation {self._reservation_id} cancelled. Reason: {reason}")
        return True
    
    def get_info(self) -> dict:
        return {
            "reservation_id": self._reservation_id,
            "guest": self._guest.name,
            "room": self._room.room_number,
            "room_type": self._room.room_type.value,
            "check_in": self._check_in_date.strftime("%Y-%m-%d"),
            "check_out": self._check_out_date.strftime("%Y-%m-%d"),
            "nights": self.get_nights(),
            "status": self._status.value,
            "special_requests": self._special_requests,
            "estimated_total": f"${self._room.price_per_night * self.get_nights():.2f}"
        }
    
    def __str__(self):
        return f"Reservation {self._reservation_id} - {self._guest.name}"


# --------------------------------------------
# HOTEL MANAGEMENT SYSTEM (MAIN CONTROLLER)
# --------------------------------------------
class HotelManagementSystem:
    """
    Central controller for all hotel operations.
    
    SINGLETON-LIKE: Typically one instance manages the entire hotel.
    FACADE: Provides unified interface to rooms, guests, reservations.
    """
    
    def __init__(self, hotel_name: str, address: str):
        self._hotel_name = hotel_name
        self._address = address
        
        # Data stores
        self._rooms: dict[str, Room] = {}
        self._guests: dict[str, Guest] = {}
        self._reservations: dict[str, Reservation] = {}
        self._services: dict[str, Service] = {}
        
        # Auto-increment counters
        self._next_guest_id = 1
        self._next_reservation_id = 1
        self._next_service_id = 1
    
    def _generate_guest_id(self) -> str:
        id_str = f"G{self._next_guest_id:05d}"
        self._next_guest_id += 1
        return id_str
    
    def _generate_reservation_id(self) -> str:
        id_str = f"R{self._next_reservation_id:05d}"
        self._next_reservation_id += 1
        return id_str
    
    # ========== ROOM MANAGEMENT ==========
    
    def add_room(self, room_number: str, room_type: RoomType, 
                 floor: int, price_override: Optional[float] = None) -> Room:
        """Add a new room to the hotel."""
        if room_number in self._rooms:
            raise ValueError(f"Room {room_number} already exists")
        
        room = Room(room_number, room_type, floor, price_override)
        self._rooms[room_number] = room
        print(f"✓ Added {room}")
        return room
    
    def get_room(self, room_number: str) -> Optional[Room]:
        """Get a room by number."""
        return self._rooms.get(room_number)
    
    def get_available_rooms(self, room_type: Optional[RoomType] = None,
                           check_in: Optional[datetime] = None,
                           check_out: Optional[datetime] = None) -> list[Room]:
        """Get list of available rooms, optionally filtered."""
        available = [r for r in self._rooms.values() if r.is_available]
        
        if room_type:
            available = [r for r in available if r.room_type == room_type]
        
        # TODO: Check against existing reservations for date range
        
        return available
    
    def list_all_rooms(self) -> list[Room]:
        """List all rooms in the hotel."""
        return list(self._rooms.values())
    
    # ========== GUEST MANAGEMENT ==========
    
    def register_guest(self, name: str, email: str, phone: str,
                       id_type: str, id_number: str) -> Guest:
        """Register a new guest."""
        guest_id = self._generate_guest_id()
        guest = Guest(guest_id, name, email, phone, id_type, id_number)
        self._guests[guest_id] = guest
        print(f"✓ Guest registered: {guest}")
        return guest
    
    def get_guest(self, guest_id: str) -> Optional[Guest]:
        """Find a guest by ID."""
        return self._guests.get(guest_id)
    
    def search_guests(self, search_term: str) -> list[Guest]:
        """Search guests by name or email."""
        search_term = search_term.lower()
        return [g for g in self._guests.values()
                if search_term in g.name.lower() or search_term in g._email.lower()]
    
    # ========== RESERVATION MANAGEMENT ==========
    
    def create_reservation(self, guest: Guest, room: Room,
                          check_in: datetime, check_out: datetime) -> Reservation:
        """Create a new reservation."""
        if not room.is_available:
            raise ValueError(f"Room {room.room_number} is not available")
        
        reservation_id = self._generate_reservation_id()
        reservation = Reservation(reservation_id, guest, room, check_in, check_out)
        self._reservations[reservation_id] = reservation
        
        print(f"✓ Reservation created: {reservation_id}")
        print(f"  Guest: {guest.name}")
        print(f"  Room: {room.room_number} ({room.room_type.value})")
        print(f"  Dates: {check_in.strftime('%Y-%m-%d')} to {check_out.strftime('%Y-%m-%d')}")
        print(f"  Estimated: ${room.price_per_night * reservation.get_nights():.2f}")
        
        return reservation
    
    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Find a reservation by ID."""
        return self._reservations.get(reservation_id)
    
    def get_active_reservations(self) -> list[Reservation]:
        """Get all active (not cancelled/completed) reservations."""
        active_statuses = [
            ReservationStatus.PENDING,
            ReservationStatus.CONFIRMED,
            ReservationStatus.CHECKED_IN
        ]
        return [r for r in self._reservations.values() 
                if r.status in active_statuses]
    
    def get_todays_checkouts(self) -> list[Reservation]:
        """Get reservations checking out today."""
        today = datetime.now().date()
        return [r for r in self._reservations.values()
                if r.status == ReservationStatus.CHECKED_IN
                and r._check_out_date.date() == today]
    
    # ========== SERVICE MANAGEMENT ==========
    
    def add_service(self, name: str, description: str, price: float) -> Service:
        """Add a new service to the hotel."""
        service_id = f"SVC{self._next_service_id:03d}"
        self._next_service_id += 1
        
        service = Service(service_id, name, description, price)
        self._services[service_id] = service
        print(f"✓ Service added: {name} - ${price:.2f}")
        return service
    
    def get_service(self, service_id: str) -> Optional[Service]:
        """Get a service by ID."""
        return self._services.get(service_id)
    
    def list_services(self) -> list[Service]:
        """List all available services."""
        return list(self._services.values())
    
    def charge_service_to_room(self, reservation: Reservation, 
                               service: Service, quantity: int = 1):
        """Add a service charge to a guest's bill."""
        if reservation.bill is None:
            print("Error: Guest must be checked in to charge services")
            return False
        
        reservation.bill.add_service_charge(service, quantity)
        return True
    
    # ========== REPORTS ==========
    
    def get_occupancy_report(self) -> dict:
        """Generate occupancy statistics."""
        total_rooms = len(self._rooms)
        occupied = len([r for r in self._rooms.values() 
                       if r.status == RoomStatus.OCCUPIED])
        available = len([r for r in self._rooms.values() 
                        if r.status == RoomStatus.AVAILABLE])
        maintenance = len([r for r in self._rooms.values() 
                          if r.status == RoomStatus.MAINTENANCE])
        
        occupancy_rate = (occupied / total_rooms * 100) if total_rooms > 0 else 0
        
        # Breakdown by room type
        by_type = {}
        for room_type in RoomType:
            rooms_of_type = [r for r in self._rooms.values() 
                           if r.room_type == room_type]
            occupied_of_type = [r for r in rooms_of_type 
                               if r.status == RoomStatus.OCCUPIED]
            by_type[room_type.value] = {
                "total": len(rooms_of_type),
                "occupied": len(occupied_of_type)
            }
        
        return {
            "total_rooms": total_rooms,
            "occupied": occupied,
            "available": available,
            "maintenance": maintenance,
            "occupancy_rate": f"{occupancy_rate:.1f}%",
            "by_room_type": by_type
        }
    
    def get_revenue_report(self, start_date: datetime = None, 
                          end_date: datetime = None) -> dict:
        """Generate revenue report."""
        completed = [r for r in self._reservations.values()
                    if r.status == ReservationStatus.CHECKED_OUT and r.bill]
        
        if start_date:
            completed = [r for r in completed 
                        if r._actual_check_out >= start_date]
        if end_date:
            completed = [r for r in completed 
                        if r._actual_check_out <= end_date]
        
        total_revenue = sum(r.bill.calculate_total() for r in completed)
        room_revenue = sum(
            sum(item["total"] for item in r.bill._line_items 
                if item["category"] == "Room")
            for r in completed
        )
        service_revenue = total_revenue - room_revenue
        
        return {
            "total_reservations": len(completed),
            "total_revenue": f"${total_revenue:.2f}",
            "room_revenue": f"${room_revenue:.2f}",
            "service_revenue": f"${service_revenue:.2f}",
            "average_per_stay": f"${(total_revenue/len(completed)):.2f}" if completed else "$0.00"
        }
    
    def get_hotel_status(self) -> dict:
        """Get overall hotel status summary."""
        return {
            "hotel_name": self._hotel_name,
            "address": self._address,
            "total_rooms": len(self._rooms),
            "total_guests": len(self._guests),
            "active_reservations": len(self.get_active_reservations()),
            "services_offered": len(self._services),
            "occupancy": self.get_occupancy_report()
        }


# ============================================
# DEMONSTRATION / USAGE EXAMPLE
# ============================================

def main():
    """Demonstrate the Hotel Management System."""
    
    print("=" * 60)
    print("HOTEL MANAGEMENT SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize hotel
    hotel = HotelManagementSystem(
        "Grand Plaza Hotel",
        "123 Luxury Avenue, Downtown"
    )
    
    # ----- Setup Rooms -----
    print("\n🏨 SETTING UP ROOMS...")
    
    # Floor 1 - Standard rooms
    hotel.add_room("101", RoomType.SINGLE, 1)
    hotel.add_room("102", RoomType.SINGLE, 1)
    hotel.add_room("103", RoomType.DOUBLE, 1)
    hotel.add_room("104", RoomType.DOUBLE, 1)
    
    # Floor 2 - Premium rooms
    hotel.add_room("201", RoomType.SUITE, 2)
    hotel.add_room("202", RoomType.SUITE, 2)
    hotel.add_room("203", RoomType.DELUXE, 2)
    
    # Floor 3 - Luxury
    hotel.add_room("301", RoomType.PRESIDENTIAL, 3, 750)  # Custom price
    
    # ----- Add Services -----
    print("\n🍽️ ADDING SERVICES...")
    room_service = hotel.add_service(
        "Room Service", "24-hour in-room dining", 15.00
    )
    spa = hotel.add_service(
        "Spa Treatment", "1-hour relaxation massage", 120.00
    )
    laundry = hotel.add_service(
        "Laundry Service", "Same-day laundry and dry cleaning", 25.00
    )
    airport_transfer = hotel.add_service(
        "Airport Transfer", "Luxury car to/from airport", 75.00
    )
    
    # ----- Register Guests -----
    print("\n👥 REGISTERING GUESTS...")
    guest1 = hotel.register_guest(
        "John Smith", "john.smith@email.com", "555-1234",
        "Passport", "AB123456"
    )
    guest2 = hotel.register_guest(
        "Emma Johnson", "emma.j@email.com", "555-5678",
        "Driver's License", "DL789012"
    )
    
    # Make guest2 a VIP (for demo)
    guest2._vip_status = True
    guest2._loyalty_points = 15000
    
    # ----- Create Reservations -----
    print("\n📅 CREATING RESERVATIONS...")
    
    suite = hotel.get_room("201")
    deluxe = hotel.get_room("203")
    
    # Get dates
    check_in_1 = datetime.now()
    check_out_1 = datetime.now() + timedelta(days=3)
    
    check_in_2 = datetime.now()
    check_out_2 = datetime.now() + timedelta(days=5)
    
    res1 = hotel.create_reservation(guest1, suite, check_in_1, check_out_1)
    res2 = hotel.create_reservation(guest2, deluxe, check_in_2, check_out_2)
    
    # ----- Confirm and Check-in -----
    print("\n✅ CONFIRMING RESERVATIONS...")
    res1.confirm()
    res2.confirm()
    
    print("\n🔑 CHECKING IN GUESTS...")
    res1.check_in()
    res2.check_in()
    
    # ----- Add Services to Bills -----
    print("\n🛎️ ADDING SERVICES...")
    hotel.charge_service_to_room(res1, room_service, 2)  # 2 room service orders
    hotel.charge_service_to_room(res1, spa, 1)
    hotel.charge_service_to_room(res2, airport_transfer, 2)  # Round trip
    hotel.charge_service_to_room(res2, laundry, 1)
    
    # ----- Check-out Guest 1 -----
    print("\n🚪 CHECKING OUT GUEST...")
    bill1 = res1.check_out()
    
    if bill1:
        # Print invoice
        bill1.print_invoice()
        
        # Process payment
        print("\n💳 PROCESSING PAYMENT...")
        bill1.add_payment(bill1.calculate_total(), PaymentMethod.CREDIT_CARD)
    
    # ----- Reports -----
    print("\n" + "=" * 60)
    print("📊 REPORTS")
    print("=" * 60)
    
    # Guest Info
    print("\n--- Guest Info: Emma Johnson ---")
    for key, value in guest2.get_info().items():
        print(f"  {key}: {value}")
    
    # Room Status
    print("\n--- Available Rooms ---")
    available = hotel.get_available_rooms()
    for room in available:
        print(f"  {room.room_number}: {room.room_type.value} - ${room.price_per_night}/night")
    
    # Occupancy Report
    print("\n--- Occupancy Report ---")
    occupancy = hotel.get_occupancy_report()
    print(f"  Total Rooms: {occupancy['total_rooms']}")
    print(f"  Occupied: {occupancy['occupied']}")
    print(f"  Available: {occupancy['available']}")
    print(f"  Occupancy Rate: {occupancy['occupancy_rate']}")
    
    # Hotel Status
    print("\n--- Hotel Status ---")
    status = hotel.get_hotel_status()
    for key, value in status.items():
        if key != "occupancy":
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
