const TAX_RATE = 1.08;

function processActiveItems(local_items) {
  return local_items
    .filter(local_item => local_item.active)
    .map(local_item => ({
      name: local_item.n,
      final_price: local_item.price * TAX_RATE
    }));
}

// example data
const data = [{n: "Laptop", active: true, price: 1000}, {n: "Mouse", active: false, price: 25}];
console.log(process(data));