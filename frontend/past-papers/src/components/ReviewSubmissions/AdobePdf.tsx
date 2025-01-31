/*
Copyright 2020 Adobe
All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in
accordance with the terms of the Adobe license agreement accompanying
it. If you have received this file from a source other than Adobe,
then your use, modification, or distribution of it requires the prior
written permission of Adobe.
*/

import { Component } from "react";
import ViewSDKClient from "./ViewSDKClient";

class AdobePDF extends Component {
  componentDidMount() {
    const viewSDKClient = new ViewSDKClient();
    viewSDKClient.ready().then(() => {
      /* Invoke file preview */
      viewSDKClient.previewFile(
        "pdf-div",
        {
          /* Pass the embed mode option here */
          embedMode: "IN_LINE",
        },
        this.props.url
      );
    });
  }

  render() {
    return (
      <>
        <div className="lg:mr-8 mb-8  w-full lg:w-[70%]">
          <h1 className=" text-center mb-2 text-xl">
            {this.props.name &&
              this.props.email &&
              `Submitted by ${this.props.name} (${this.props.email})`}
          </h1>
          <div id="pdf-div" className="w-full h-[33rem] lg:h-[95%] "></div>
        </div>
      </>
    );
  }
}

export default AdobePDF;
