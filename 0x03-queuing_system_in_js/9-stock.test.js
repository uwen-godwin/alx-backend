import request from 'supertest';
import app from './9-stock.js';
import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();
const reserveStockAsync = promisify(client.set).bind(client);
const getStockAsync = promisify(client.get).bind(client);

describe('Stock Management API', () => {
  before(async () => {
    await reserveStockAsync('item_1', 4);
    await reserveStockAsync('item_2', 10);
    await reserveStockAsync('item_3', 2);
    await reserveStockAsync('item_4', 5);
  });

  after(async () => {
    await client.flushdbAsync();
  });

  it('should list all products', async () => {
    const res = await request(app).get('/list_products');
    expect(res.status).toBe(200);
    expect(res.body).toHaveLength(4);
    expect(res.body[0]).toHaveProperty('itemId', 1);
    expect(res.body[0]).toHaveProperty('itemName', 'Suitcase 250');
  });

  it('should return product by ID', async () => {
    const res = await request(app).get('/list_products/1');
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty('itemId', 1);
    expect(res.body).toHaveProperty('itemName', 'Suitcase 250');
  });

  it('should reserve stock', async () => {
    const res = await request(app).post('/reserve_product/1');
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty('itemId', 1);
    expect(res.body).toHaveProperty('status', 'Reservation confirmed');
  });

  it('should fail to reserve stock if out of stock', async () => {
    await reserveStockAsync('item_3', 0);
    const res = await request(app).post('/reserve_product/3');
    expect(res.status).toBe(404);
    expect(res.body).toHaveProperty('error', 'Out of stock');
  });
});
