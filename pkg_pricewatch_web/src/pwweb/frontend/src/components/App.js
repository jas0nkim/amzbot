import React, { Component } from "react"
import AddUrl from "./AddUrl.js"
import ProductList from "./ProductList.js"

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      products: [
        {
          id: 'test01',
          title: 'GERBER LIL’ CRUNCHIES, Mild Cheddar, Toddler Snacks | Walmart Canada',
          image: 'https://i5.walmartimages.ca/images/Large/109/7_2/999999-15000141097_2.jpg',
          description: 'Buy GERBER LIL’ CRUNCHIES, Mild Cheddar, Toddler Snacks from Walmart Canada. Shop for more Baby Snacks & Finger Foods  available online at Walmart.ca',
          price: 2.77,
          stock: 119,
        },
        {
          id: 'test02',
          title: 'GERBER LIL’ CRUNCHIES, Mild Cheddar, Toddler Snacks | Walmart Canada',
          image: 'https://i5.walmartimages.ca/images/Large/109/7_2/999999-15000141097_2.jpg',
          description: 'Buy GERBER LIL’ CRUNCHIES, Mild Cheddar, Toddler Snacks from Walmart Canada. Shop for more Baby Snacks & Finger Foods  available online at Walmart.ca',
          price: 2.77,
          stock: 119,
        }
      ]
    };
  }
  
  render() {
    return (
      <div>
        <AddUrl />
        <ProductList products={this.state.products} />
      </div>
    );
  }
}
  
export default App;
  