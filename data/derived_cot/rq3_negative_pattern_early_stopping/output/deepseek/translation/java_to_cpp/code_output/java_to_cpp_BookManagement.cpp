using System;
using System.Collections.Generic;

namespace BookManagement {
    public class BookManagement {
        private Dictionary<string, int> inventory;

        public BookManagement() {
            this.inventory = new Dictionary<string, int>();
        }

        public void AddBook(string title, int quantity) {
            // C# Dictionary doesn't have [] with default value, so explicit check
            if (this.inventory.ContainsKey(title)) {
                this.inventory[title] = this.inventory[title] + quantity;
            } else {
                this.inventory[title] = quantity;
            }
        }

        public void RemoveBook(string title, int quantity) {
            // Check if title exists and quantity is sufficient
            if (!this.inventory.ContainsKey(title) || this.inventory[title] < quantity) {
                throw new Exception("Invalid operation");
            }
            int newQuantity = this.inventory[title] - quantity;
            if (newQuantity == 0) {
                this.inventory.Remove(title);
            } else {
                this.inventory[title] = newQuantity;
            }
        }

        public Dictionary<string, int> ViewInventory() {
            // Return a shallow copy (since value type int, this is a copy)
            return new Dictionary<string, int>(this.inventory);
        }

        public int ViewBookQuantity(string title) {
            // TryGetValue avoids double lookup
            if (this.inventory.TryGetValue(title, out int quantity)) {
                return quantity;
            }
            return 0;
        }
    }
}