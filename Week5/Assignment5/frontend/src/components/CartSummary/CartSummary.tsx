import { useCart } from "../../context/CartContext";
import { useCartSummary } from "./useCartSummary";
import "./CartSummary.css";

export default function CartSummary() {
  const { removeItem } = useCart();
  const { items, total, error, placing, placeOrder } = useCartSummary();

  if (items.length === 0) {
    return (
      <div className="cart-summary card">
        <h3>Your Cart</h3>
        <p className="cart-empty">No items added yet.</p>
      </div>
    );
  }

  return (
    <div className="cart-summary card">
      <h3>Your Cart</h3>
      {items.map((item) => (
        <div key={item.food_item_id} className="cart-line">
          <span>{item.name} × {item.quantity}</span>
          <span>
            ₹{(item.price * item.quantity).toFixed(2)}
            <button className="cart-remove" onClick={() => removeItem(item.food_item_id)}>✕</button>
          </span>
        </div>
      ))}
      <div className="cart-total">
        <strong>Total</strong>
        <strong>₹{total.toFixed(2)}</strong>
      </div>
      {error && <p className="error-text">{error}</p>}
      <button className="btn" style={{ width: "100%" }} disabled={placing} onClick={placeOrder}>
        {placing ? "Placing order..." : "Place Order"}
      </button>
    </div>
  );
}
