import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Create Redis client
const client = redis.createClient();
const reserveStockAsync = promisify(client.set).bind(client);
const getStockAsync = promisify(client.get).bind(client);

const app = express();
const port = 1245;

// Sample products
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

// Middleware to return JSON
app.use(express.json());

// List all products
app.get('/list_products', (req, res) => {
  res.json(listProducts.map(({ id, name, price, stock }) => ({
    itemId: id,
    itemName: name,
    price,
    initialAvailableQuantity: stock
  })));
});

// Get product by ID
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = listProducts.find((p) => p.id === itemId);

  if (!product) {
    return res.status(404).json({ error: 'Product not found' });
  }

  const currentStock = await getStockAsync(`item_${itemId}`);
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    currentQuantity: parseInt(currentStock, 10) || product.stock
  });
});

// Reserve stock
app.post('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = listProducts.find((p) => p.id === itemId);

  if (!product) {
    return res.status(404).json({ error: 'Product not found' });
  }

  const currentStock = await getStockAsync(`item_${itemId}`);
  const stock = parseInt(currentStock, 10) || product.stock;

  if (stock <= 0) {
    return res.status(404).json({ error: 'Out of stock' });
  }

  await reserveStockAsync(`item_${itemId}`, stock - 1);
  res.json({ itemId: product.id, itemName: product.name, status: 'Reservation confirmed' });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

export default app;
