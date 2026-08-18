import { useOrders } from "./useOrders";
import "./Orders.css";

const STATUS_CLASS: Record<string, string> = {
  pending: "status-pending",
  confirmed: "status-confirmed",
  delivered: "status-delivered",
  cancelled: "status-cancelled",
};

export default function Orders() {
  const { orders, loading, error } = useOrders();

  if (loading) return <div className="page">Loading orders...</div>;
  if (error) return <div className="page error-text">{error}</div>;
  if (orders.length === 0) return <div className="page">You haven't placed any orders yet.</div>;

  return (
    <div className="page">
      <h2>My Orders</h2>
      {orders.map((order) => (
        <div key={order.order_id} className="card order-card">
          <div className="order-header">
            <strong>Order #{order.order_id}</strong>
            <span className={`order-status ${STATUS_CLASS[order.order_status]}`}>
              {order.order_status}
            </span>
          </div>
          <ul className="order-items">
            {order.items.map((item) => (
              <li key={item.food_item_id}>
                {item.name} × {item.quantity} - ₹{(item.price_at_order * item.quantity).toFixed(2)}
              </li>
            ))}
          </ul>
          <div className="order-footer">
            <span>{new Date(order.created_at).toLocaleString()}</span>
            <strong>Total: ₹{order.total_amount.toFixed(2)}</strong>
          </div>
        </div>
      ))}
    </div>
  );
}
