import AdaWidgetSDK from "@ada-support/ada-widget-sdk";

const widgetSDK = new AdaWidgetSDK();

const containerElement = document.getElementById("widget-container");
const sdkInputElement = document.getElementById("widget-input-data");
const inputElement = document.getElementById("input-field");
const submitButtonElement = document.getElementById("submit-button");
const submitMessageElement = document.getElementById("submit-message");

submitButtonElement.onclick = () => {
  widgetSDK.sendUserData({
    responseData: inputElement.value
  }, (event) => {
    if (event.type === "SEND_USER_DATA_SUCCESS") {
      submitMessageElement.innerText = "Data was successfully submitted";
      submitButtonElement.disabled = true;
    } else {
      submitMessageElement.innerText = "Data submission failed, please try again";
    }
  });
};

widgetSDK.init((event) => {
  if (!widgetSDK.widgetIsActive) {
    containerElement.innerHTML = "The widget is not active";
    return;
  }

  const { inputdata } = widgetSDK.metaData;

  sdkInputElement.innerHTML = inputdata;
});
