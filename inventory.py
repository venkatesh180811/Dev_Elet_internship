#!/usr/bin/env python3
"""
Simple Inventory Management System
A console-based tool for managing product inventory with CRUD operations.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


class Product:
    """Represents a product in the inventory."""
    
    def __init__(self, name: str, quantity: int, price: float, category: str = "General"):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at
    
    def to_dict(self) -> Dict:
        """Convert product to dictionary for storage."""
        return {
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create product from dictionary."""
        product = cls(data['name'], data['quantity'], data['price'], data.get('category', 'General'))
        product.created_at = data.get('created_at', product.created_at)
        product.updated_at = data.get('updated_at', product.updated_at)
        return product
    
    def update_timestamp(self):
        """Update the last modified timestamp."""
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class InventoryManager:
    """Main inventory management class."""
    
    def __init__(self, data_file: str = "inventory.json"):
        self.data_file = data_file
        self.inventory: Dict[str, Product] = {}
        self.load_inventory()
    
    def load_inventory(self):
        """Load inventory from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for product_name, product_data in data.items():
                        self.inventory[product_name] = Product.from_dict(product_data)
                print(f"✓ Loaded {len(self.inventory)} products from {self.data_file}")
            else:
                print(f"No existing inventory file found. Starting fresh.")
        except Exception as e:
            print(f"Error loading inventory: {e}")
    
    def save_inventory(self):
        """Save inventory to JSON file."""
        try:
            data = {name: product.to_dict() for name, product in self.inventory.items()}
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Inventory saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    def add_product(self, name: str, quantity: int, price: float, category: str = "General"):
        """Add a new product or update existing product quantity."""
        name = name.strip().lower()
        
        if name in self.inventory:
            # Product exists, update quantity
            self.inventory[name].quantity += quantity
            self.inventory[name].update_timestamp()
            print(f"✓ Updated {name}: added {quantity} units. New total: {self.inventory[name].quantity}")
        else:
            # New product
            self.inventory[name] = Product(name, quantity, price, category)
            print(f"✓ Added new product: {name} (Qty: {quantity}, Price: ${price:.2f})")
        
        self.save_inventory()
    
    def view_product(self, name: str) -> Optional[Product]:
        """View details of a specific product."""
        name = name.strip().lower()
        
        if name in self.inventory:
            product = self.inventory[name]
            print(f"\n--- Product Details ---")
            print(f"Name: {product.name.title()}")
            print(f"Quantity: {product.quantity}")
            print(f"Price: ${product.price:.2f}")
            print(f"Category: {product.category}")
            print(f"Total Value: ${product.quantity * product.price:.2f}")
            print(f"Created: {product.created_at}")
            print(f"Last Updated: {product.updated_at}")
            return product
        else:
            print(f"❌ Product '{name}' not found in inventory.")
            return None
    
    def view_all_products(self):
        """Display all products in inventory."""
        if not self.inventory:
            print("📦 Inventory is empty.")
            return
        
        print(f"\n--- Inventory Summary ({len(self.inventory)} products) ---")
        print(f"{'Product':<20} {'Quantity':<10} {'Price':<10} {'Category':<15} {'Total Value':<12}")
        print("-" * 77)
        
        total_value = 0
        for product in sorted(self.inventory.values(), key=lambda p: p.name):
            product_value = product.quantity * product.price
            total_value += product_value
            
            print(f"{product.name.title():<20} {product.quantity:<10} "
                  f"${product.price:<9.2f} {product.category:<15} ${product_value:<11.2f}")
        
        print("-" * 77)
        print(f"{'TOTAL INVENTORY VALUE:':<67} ${total_value:.2f}")
    
    def update_product(self, name: str, quantity: int = None, price: float = None, category: str = None):
        """Update product details."""
        name = name.strip().lower()
        
        if name not in self.inventory:
            print(f"❌ Product '{name}' not found in inventory.")
            return
        
        product = self.inventory[name]
        updated = False
        
        if quantity is not None:
            product.quantity = quantity
            updated = True
            print(f"✓ Updated quantity to {quantity}")
        
        if price is not None:
            product.price = price
            updated = True
            print(f"✓ Updated price to ${price:.2f}")
        
        if category is not None:
            product.category = category
            updated = True
            print(f"✓ Updated category to {category}")
        
        if updated:
            product.update_timestamp()
            self.save_inventory()
            print(f"✓ Product '{name.title()}' updated successfully.")
        else:
            print("No changes made.")
    
    def remove_product(self, name: str, quantity: int = None):
        """Remove product or reduce quantity."""
        name = name.strip().lower()
        
        if name not in self.inventory:
            print(f"❌ Product '{name}' not found in inventory.")
            return
        
        product = self.inventory[name]
        
        if quantity is None:
            # Remove entire product
            del self.inventory[name]
            print(f"✓ Removed '{name.title()}' completely from inventory.")
        else:
            # Reduce quantity
            if quantity >= product.quantity:
                del self.inventory[name]
                print(f"✓ Removed all {product.quantity} units of '{name.title()}' from inventory.")
            else:
                product.quantity -= quantity
                product.update_timestamp()
                print(f"✓ Removed {quantity} units of '{name.title()}'. Remaining: {product.quantity}")
        
        self.save_inventory()
    
    def search_products(self, query: str):
        """Search products by name or category."""
        query = query.strip().lower()
        matches = []
        
        for product in self.inventory.values():
            if (query in product.name.lower() or 
                query in product.category.lower()):
                matches.append(product)
        
        if matches:
            print(f"\n--- Search Results for '{query}' ({len(matches)} found) ---")
            print(f"{'Product':<20} {'Quantity':<10} {'Price':<10} {'Category':<15}")
            print("-" * 65)
            
            for product in sorted(matches, key=lambda p: p.name):
                print(f"{product.name.title():<20} {product.quantity:<10} "
                      f"${product.price:<9.2f} {product.category:<15}")
        else:
            print(f"❌ No products found matching '{query}'.")
    
    def low_stock_alert(self, threshold: int = 5):
        """Show products with low stock."""
        low_stock = [p for p in self.inventory.values() if p.quantity <= threshold]
        
        if low_stock:
            print(f"\n Low Stock Alert (≤ {threshold} units):")
            print(f"{'Product':<20} {'Quantity':<10} {'Category':<15}")
            print("-" * 45)
            
            for product in sorted(low_stock, key=lambda p: p.quantity):
                print(f"{product.name.title():<20} {product.quantity:<10} {product.category:<15}")
        else:
            print(f"✓ No products with low stock (≤ {threshold} units).")


def get_input(prompt: str, input_type=str, validator=None):
    """Get validated input from user."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Input cannot be empty. Please try again.")
                continue
            
            if input_type != str:
                value = input_type(value)
            
            if validator and not validator(value):
                print("Invalid input. Please try again.")
                continue
            
            return value
        except ValueError:
            print(f"Invalid {input_type.__name__}. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("     INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Product")
    print("2. View All Products")
    print("3. View Specific Product")
    print("4. Update Product")
    print("5. Remove Product")
    print("6. Search Products")
    print("7. Low Stock Alert")
    print("8. Exit")
    print("-"*50)


def main():
    """Main application loop."""
    print(" Welcome to the Inventory Management System!")
    
    # Initialize inventory manager
    inventory = InventoryManager()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                # Add Product
                print("\n--- Add New Product ---")
                name = get_input("Product name: ")
                if name is None:
                    continue
                
                quantity = get_input("Quantity: ", int, lambda x: x >= 0)
                if quantity is None:
                    continue
                
                price = get_input("Price ($): ", float, lambda x: x >= 0)
                if price is None:
                    continue
                
                category = input("Category (optional, press Enter for 'General'): ").strip()
                if not category:
                    category = "General"
                
                inventory.add_product(name, quantity, price, category)
            
            elif choice == '2':
                # View All Products
                inventory.view_all_products()
            
            elif choice == '3':
                # View Specific Product
                name = get_input("Enter product name: ")
                if name is not None:
                    inventory.view_product(name)
            
            elif choice == '4':
                # Update Product
                print("\n--- Update Product ---")
                name = get_input("Enter product name: ")
                if name is None:
                    continue
                
                if inventory.view_product(name) is None:
                    continue
                
                print("\nLeave blank to keep current value:")
                
                quantity_str = input("New quantity: ").strip()
                quantity = int(quantity_str) if quantity_str else None
                
                price_str = input("New price: ").strip()
                price = float(price_str) if price_str else None
                
                category = input("New category: ").strip()
                category = category if category else None
                
                inventory.update_product(name, quantity, price, category)
            
            elif choice == '5':
                # Remove Product
                print("\n--- Remove Product ---")
                name = get_input("Enter product name: ")
                if name is None:
                    continue
                
                if inventory.view_product(name) is None:
                    continue
                
                remove_all = input("Remove entire product? (y/n, default: y): ").strip().lower()
                
                if remove_all == 'n':
                    quantity = get_input("Quantity to remove: ", int, lambda x: x > 0)
                    if quantity is not None:
                        inventory.remove_product(name, quantity)
                else:
                    confirm = input(f"Confirm removal of '{name}'? (y/n): ").strip().lower()
                    if confirm == 'y':
                        inventory.remove_product(name)
            
            elif choice == '6':
                # Search Products
                query = get_input("Enter search term (name or category): ")
                if query is not None:
                    inventory.search_products(query)
            
            elif choice == '7':
                # Low Stock Alert
                threshold_str = input("Enter low stock threshold (default: 5): ").strip()
                threshold = int(threshold_str) if threshold_str else 5
                inventory.low_stock_alert(threshold)
            
            elif choice == '8':
                # Exit
                print("\n Thank you for using the Inventory Management System!")
                print("Your inventory has been saved automatically.")
                break
            
            else:
                print("❌ Invalid choice. Please enter a number between 1-8.")
        
        except KeyboardInterrupt:
            print("\n\n Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()