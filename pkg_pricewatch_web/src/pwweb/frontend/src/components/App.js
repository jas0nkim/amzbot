import React, { Component } from "react"
import AddUrl from './AddUrl.js'
import ProductList from './ProductList.js'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  
  render() {
    return (
      <div>
        <AddUrl></AddUrl>
        <ProductList></ProductList>
      </div>
    );
  }
}
  
export default App;
  