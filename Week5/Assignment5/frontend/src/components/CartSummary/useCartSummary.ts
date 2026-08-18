import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosClient from "../../api/axiosClient";
import { useCart } from "../../context/CartContext";
import { useAuth } from "../../context/AuthContext";

export function useCartSummary() {
  const { items, total, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [placing, setPlacing] = useState(false);

  async function placeOrder() {
    setError("");

    if (!user) {
      navigate("/login");
      return;
    }
    if (items.length === 0) return;

    setPlacing(true);
    try {
      await axiosClient.post("/orders", {
        restaurant_id: items[0].restaurant_id,
        items: items.map((i) => ({ food_item_id: i.food_item_id, quantity: i.quantity })),
        payment_method: "upi",
      });
      clearCart();
      navigate("/orders");
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to place order");
    } finally {
      setPlacing(false);
    }
  }

  return { items, total, error, placing, placeOrder };
}
