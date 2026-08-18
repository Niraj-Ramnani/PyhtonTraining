import FoodItemCard from "../../components/FoodItemCard/FoodItemCard";
import CartSummary from "../../components/CartSummary/CartSummary";
import { useCart } from "../../context/CartContext";
import { useMenu } from "./useMenu";
import "./Menu.css";

export default function Menu() {
  const { restaurant, items, loading, error } = useMenu();
  const { addItem } = useCart();

  if (loading) return <div className="page">Loading menu...</div>;
  if (error) return <div className="page error-text">{error}</div>;

  return (
    <div className="page menu-page">
      <div className="menu-items">
        <h2>{restaurant?.name}</h2>
        <p className="menu-address">{restaurant?.address}</p>
        {items.map((item) => (
          <FoodItemCard key={item.food_item_id} item={item} onAdd={addItem} />
        ))}
      </div>
      <div className="menu-cart">
        <CartSummary />
      </div>
    </div>
  );
}
