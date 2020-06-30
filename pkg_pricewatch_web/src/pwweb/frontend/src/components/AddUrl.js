import React, { Component } from "react"

class AddUrl extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  
  render() {
    return (
      <div className="mb-2">
        <form>
          <div className="form-group">
            <input type="url" className="form-control" placeholder="Enter product URL" />
          </div>
          <button type="submit" className="btn btn-primary">Add</button>
        </form>
      </div>
    );
  }
}
  
export default AddUrl;
  