export interface User {
  user_id: number;
  name: string;
  email: string;
  role: string;
}

export interface Restaurant {
  restaurant_id: number;
  name: string;
  address: string;
  phone: string;
  rating: number;
}

export interface Category {
  category_id: number;
  category_name: string;
}

export interface FoodItem {
  food_item_id: number;
  restaurant_id: number;
  category_id: number;
  category_name: string;
  name: string;
  price: number;
  is_available: number;
}

export interface CartItem {
  food_item_id: number;
  name: string;
  price: number;
  quantity: number;
  restaurant_id: number;
}

export interface OrderItem {
  food_item_id: number;
  name: string;
  quantity: number;
  price_at_order: number;
}

export interface Order {
  order_id: number;
  user_id: number;
  restaurant_id: number;
  order_status: string;
  total_amount: number;
  created_at: string;
  items: OrderItem[];
}

export interface Profile {
  user_id: number;
  name: string;
  email: string;
  phone: string | null;
  role_name: string;
  created_at: string;
}
