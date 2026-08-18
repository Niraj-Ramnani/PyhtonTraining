import { FoodItem } from "../../types";
import "./FoodItemCard.css";

interface Props {
  item: FoodItem;
  onAdd: (item: FoodItem) => void;
}

export default function FoodItemCard({ item, onAdd }: Props) {
  return (
    <div className="food-item-card card">
      <div>
        <h4>{item.name}</h4>
        <span className="food-item-category">{item.category_name}</span>
        <p className="food-item-price">₹{item.price.toFixed(2)}</p>
      </div>
      <button
        className="btn"
        disabled={!item.is_available}
        onClick={() => onAdd(item)}
      >
        {item.is_available ? "Add" : "Unavailable"}
      </button>
    </div>
  );
}
