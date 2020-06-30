import React, { Component } from "react"
import ProductInfo from './ProductInfo.js'

class ProjectList extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <ProductInfo />
        <ProductInfo />
        <ProductInfo />
      </div>
    );
  }
}
  
export default ProjectList;
