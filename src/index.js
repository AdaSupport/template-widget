import AdaWidgetSDK from "@ada-support/ada-widget-sdk";

const widgetSDK = new AdaWidgetSDK();

const containerElement = document.getElementById("widget-container");
const sdkInputElement = document.getElementById("widget-input-data");
const inputElement = document.getElementById("input-field");
const submitButtonElement = document.getElementById("submit-button");
const submitMessageElement = document.getElementById("submit-message");

const handleWidgetEnd = () => {
  widgetSDK.sendUserData({
    responseData: inputElement.value
  }, (event) => {
    if (event.type === "SEND_USER_DATA_SUCCESS") {
      submitMessageElement.innerText = "Data was successfully submitted. The widget will close in a moment.";
      submitButtonElement.disabled = true;
    } else {
      submitMessageElement.innerText = "Data submission failed, please try again.";
    }
  });
  setTimeout(() => {
    widgetSDK.setWidgetClose();
  }, 2.5 * 1000);
}

submitButtonElement.onclick = handleWidgetEnd;

widgetSDK.init((event) => {
  widgetSDK.setContainerHeight(600);
  
  if (!widgetSDK.widgetIsActive) {
    containerElement.innerHTML = "The widget is not active";
    handleWidgetEnd();
    return;
  }

  const { widgetInputs } = event;
  console.log(widgetInputs);

  sdkInputElement.innerHTML = widgetInputs.inputData;
});
