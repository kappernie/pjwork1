let payStackEventCreated = false;
const RENTER = 1;
const OWNER = 2;
const AGENT = 3;

const toastHTML = `<!-- Toast container -->
<div
  class="position-absolute p-3 top-0 start-50 translate-middle"
  style="z-index: 9999"
  data-bs-delay="10000"
>
  <div
    id="myToast"
    class="toast hide"
    role="alert"
    aria-live="assertive"
    aria-atomic="true"
  >
    <div class="toast-header">
      <strong class="me-auto">Form Submission Status</strong>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="toast"
        aria-label="Close"
      ></button>
    </div>
    <div class="toast-body"></div>
  </div>
</div>`;

function convertMonths(month) {
  const years = Math.floor(month / 12); // whole years
  const rem_months = Math.round((Decimal(month / 12 - years) * 364) / 30.33);

  return `${years} ${years === 1 ? "year" : "years"} ${
    rem_months ? rem_months + (rem_months == 1 ? " month" : " months") : ""
  }`;
}
// generate option elements for rent duration

function generateSelectOptions(min_rent_duration, max_rent_duration) {
  // Initialize an empty array to store the option elements
  const options = [];

  // Start with the min_rent_duration as the initial value
  let currentValue = min_rent_duration;

  // Continue generating options until currentValue is less than or equal to max_rent_duration
  while (currentValue <= max_rent_duration) {
    // Create a new option element
    const option = document.createElement("option");
    option.value = currentValue;
    option.text = convertMonths(currentValue);

    // Add the option to the options array
    options.push(option);

    // Increment the currentValue by 6 for the next iteration
    currentValue += 6;
  }

  // Check if the last option's value is less than max_rent_duration
  if (
    options.length > 0 &&
    options[options.length - 1].value < max_rent_duration
  ) {
    // Add a new option with max_rent_duration
    const lastOption = document.createElement("option");
    lastOption.value = max_rent_duration;
    lastOption.text = convertMonths(max_rent_duration);

    // Add the last option to the options array
    options.push(lastOption);
  }

  // Return the array of generated options
  return options;
}

function generateUsername(email) {
  // Extract the part of the email before the "@" symbol
  const username = email.split("@")[0];

  // Generate a random 4-digit number to ensure uniqueness
  const uniqueIdentifier = Math.floor(Math.random() * 10000);

  // Combine the username and unique identifier
  const uniqueUsername = `${username}${uniqueIdentifier}`;

  return uniqueUsername;
}

// view more button event handler

function viewMoreEventHandler(event, viewMoreButton) {
  // console.log(viewMoreButton);
  const pk = parseInt(viewMoreButton.id); //grab the pk of the property  through element id
  $.get(`/api/listing/${pk}/`, function (data) {
    const apiResponse = data;
    console.log(apiResponse);
    pictures = document.getElementById("carousel-inner");
    property_title = document.getElementById("title");
    main_details = document.getElementById("main_details");
    other_details = document.getElementById("other_details");

    property_title.innerHTML = "";
    main_details.innerHTML = "";
    other_details.innerHTML = "";
    pictures.innerHTML = "";

    property_title.innerHTML = data.name;
    main_details.innerHTML = `Location: ${data.location_text ?? "Missing"}, ${
      data?.for_rent ? "Monthly Price:" : "Price:"
    } ${new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: data?.currency || "GHS",
    }).format(data.price)} <br> Type: ${data.property_types}, Phone Number: ${
      data?.["lister_phone"]
    } <br> ${
      data?.for_rent
        ? `Minimum Allowed Rent Duration: ${convertMonths(
            data?.min_rent_duration
          )}`
        : ""
    } <br> ${
      data?.for_rent
        ? `Maximum Allowed Rent Duration: ${convertMonths(
            data?.max_rent_duration
          )}`
        : ""
    }`;
    other_details.innerHTML = ` Description : ${data.description}`;

    data.propertyimages.forEach((propertyimage) => {
      pictures.innerHTML += `<div class="carousel-item active"><img src=${propertyimage} class="d-block w-100" alt="Gallery Image 1"></div>`;
    });

    // update the values in the generic viewmoremodal
    const viewMoreModal = new bootstrap.Modal(
      document.getElementById("viewMoreModal")
    );
    // Show the View More Modal
    viewMoreModal.show();
  });
}

// buy/Rent event handler

function buyOrRentEventHanlder(event, buyRentButton) {
  const pk = parseInt(buyRentButton.id); //grab the pk of the property  through element id
  $.get(`/api/listing/${pk}/`, function (data) {
    const apiResponse = data;
    var oneTimeRentData;
    // console.log(apiResponse);

    // document.getElementById("amount").value = apiResponse.price;

    const userDetails = JSON.parse(localStorage.getItem("remarket"));
    document.getElementById("email-address").value = userDetails.email;
    document.getElementById("first-name").value = userDetails.first_name;
    document.getElementById("last-name").value = userDetails.last_name;
    // get the details  from api ; amount of the property in this case
    // update the amount of the generic purchase template
    // Show the update purchase  Modal

    // console.log(apiResponse.for_rent);

    if (apiResponse.for_rent === true) {
      $("#buyRentModalLabel").html("Rent Property");

      $(`<div id="rent-duration" class="form-group mb-2">
  <label for="duration"
    >Choose how long you want to rent the property for</label
  >
  <select class="form-select" name="duration" id="duration" required>
    <option value="" selected disabled>
      Choose an option (6 month increments)
    </option>
  </select>
</div>`).insertAfter("#email-address-container");
      const selectOptions = generateSelectOptions(
        apiResponse?.min_rent_duration,
        apiResponse?.max_rent_duration
      );

      $("#duration").append(selectOptions);

      // add change event listener to call the api when the user selects an option to get the one-time payment amount

      $("#duration").on("change", () => {
        console.log($("#duration").val());
        $.ajax({
          type: "GET",
          url: `http://localhost:1738/api/listing/${pk}?duration=${$(
            "#duration"
          ).val()}`,
          success: function (response) {
            oneTimeRentData = response;
            // trigger radio buttons to update the value of the amount
            $("input[name='payment-plan']").change();
          },
        });
      });
      $(
        `<p id='monthly-price-renting'>Monthly price: ${new Intl.NumberFormat(
          "en-US",
          {
            style: "currency",
            currency: apiResponse?.currency || "GHS",
          }
        ).format(apiResponse?.price)}</p>`
      ).insertAfter("#rent-duration");
    } else {
      $("#buyRentModalLabel").html("Buy Property");
      $(
        `<p id='monthly-price-renting'>Price: ${new Intl.NumberFormat("en-US", {
          style: "currency",
          currency: apiResponse?.currency || "GHS",
        }).format(apiResponse?.price)}</p>`
      ).insertAfter("#email-address-container");
    }

    $("#paymentForm").append(`<div id="payment-plan" mb-3>
      <div class="form-check form-check-inline">
      <input
        class="form-check-input"
        type="radio"
        name="payment-plan"
        id="onetime"
        value="onetime"
      />
      <label class="form-check-label" for="onetime">
        OneTime Payment
      </label>
      </div>
      <div class="form-check form-check-inline">
      <input
        class="form-check-input"
        type="radio"
        name="payment-plan"
        id="recurring"
        value="recurring"
      />
      <label class="form-check-label" for="recurring">
        Recurring Payment
      </label>
      </div>
    </div>`);

    $("input[name='payment-plan']").change(() => {
      // remove the any amount elements that may be on the screen
      if ($("#onetime-amount").length) {
        $("#onetime-amount").remove();
        $("#paymentForm button").remove();
      }
      if ($("#recurring-amount").length) {
        $("#recurring-amount").remove();
        $("#paymentForm button").remove();
      }

      if ($("#onetime").is(":checked")) {
        if (apiResponse?.for_rent === true) {
          $("#paymentForm").append(
            `${
              oneTimeRentData?.amount
                ? `<p id="onetime-amount" class="mt-3">Amount: ${new Intl.NumberFormat(
                    "en-US",
                    {
                      style: "currency",
                      currency: apiResponse?.currency || "GHS",
                    }
                  ).format(oneTimeRentData?.amount)}</p>
                  
                  <button type="submit" style="width:100%;" class="btn btn-primary mt-3">Pay</button>
                  `
                : "<p id='onetime-amount' class='mt-3'><small>Please select a rent duration</small></p>"
            }`
          );
        } else {
          $("#paymentForm").append(
            `<p id="onetime-amount" class="mt-3">Amount: ${new Intl.NumberFormat(
              "en-US",
              { style: "currency", currency: apiResponse?.currency || "GHS" }
            ).format(apiResponse?.price)}</p>
            <button type="submit" style="width:100%;" class="btn btn-primary mt-3">Pay</button>
            `
          );
        }
      }

      if ($("#recurring").is(":checked")) {
        $("#paymentForm").append(
          `<div id="recurring-amount" class="mt-3"><div>Amount: ${new Intl.NumberFormat(
            "en-US",
            { style: "currency", currency: apiResponse?.currency || "GHS" }
          ).format(apiResponse?.down_payment_amt)}</div>
          ${
            apiResponse?.for_rent
              ? `<small>This amount is down payment for the first 6 months. The remaining amount will paid over a period of time based on the billing interval you choose. The scheduled payment plan will be emailed to you. Billing is automatic.</small>
                <div class="row mt-3 mb-3">
                  <label for="billingInterval" class="col-3 col-form-label">Billing Interval:</label>
                  <div class="col">
                    <select class="form-select" id="billingInterval" name="billingInterval" required>
                      <option value="" selected disabled>Choose your preferred interval</option>
                      <option value="1">Quarterly</option>
                      <option value="2">Biannually</option>
                    </select>
                  </div>
                </div>
                
                <button type="submit" style="width:100%;" class="btn btn-primary">Pay</button>
                `
              : `<small>This amount is 30% of the total price as down payment for the property. The remaining amount will be monthly installments paid over the course of the 
              mortgage duration you choose. The scheduled payment plan will be emailed to you. Billing is automatic.</small>
              <div class="row mt-3 mb-3">
                  <label for="mortgageDuration" class="col-3 col-form-label">Mortgage Duration:</label>
                  <div class="col">
                    <select class="form-select" id="mortgageDuration" name="mortgageDuration" required>
                      <option value="" selected disabled>Choose your preferred mortgage repayment duration</option>
                      <option value="12">1 year</option>
                      <option value="36">3 years</option>
                      <option value="60">5 years</option>
                    </select>
                  </div>
                </div>
              <button type="submit" style="width:100%;" class="btn btn-primary mt-3">Pay</button>
              `
          }
          </div>`
        );
      }
    });

    const buyRentModal = new bootstrap.Modal(
      document.getElementById("buyRentModal")
    );
    buyRentModal.show();

    // getters
    const getOneTimeRentData = () => oneTimeRentData;
    const getApiResponse = () => apiResponse;

    // to make sure multiple event handlers are not being attached if not the paystack modal behaves funny
    $("#paymentForm").off("submit");
    $("#paymentForm").on("submit", function (event) {
      payWithPaystack(event, getApiResponse, getOneTimeRentData);
    });
  });
}

function getCookie(key) {
  // Split the document.cookie string into an array of cookies
  const cookies = document.cookie.split(";");

  // Iterate through the cookies to find the one with the specified key
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim(); // Remove leading/trailing spaces
    const cookieParts = cookie.split("=");

    // Check if the key matches the current cookie's key
    if (cookieParts[0] === key) {
      // Return the value associated with the key
      return decodeURIComponent(cookieParts[1]);
    }
  }

  // Return null if the key is not found
  return null;
}

// Usage:
const myCookieValue = getCookie("myCookieKey");

if (myCookieValue !== null) {
  console.log(`Value of myCookieKey: ${myCookieValue}`);
} else {
  console.log("Cookie not found or key does not exist.");
}

const paymentForm = document.getElementById("paymentForm");
// paymentForm.addEventListener("submit", payWithPaystack, false);

function payWithPaystack(e, getApiResponse, getOneTimeRentData) {
  e.preventDefault();
  const paystack = new PaystackPop();
  const formData = new FormData(e.target);
  const apiResponse = getApiResponse();
  // console.log(e);

  const firstName = document.querySelector("#first-name");
  const lastName = document.querySelector("#last-name");
  const emailAddress = document.querySelector("#email-address");
  const duration = document.querySelector("#duration");
  const billingInterval = document.querySelector("#billingInterval");
  const mortgageDuration = document.querySelector("#mortgageDuration");
  console.log(apiResponse);

  const paymentPlan = formData.get("payment-plan");
  const oneTimeRentAmt = getOneTimeRentData()?.amount;
  // console.log(data.get("email-address"));
  // for (const [key, value] of formData) {
  //   console.log(key, value);
  // }

  if (apiResponse?.for_rent) {
    if (paymentPlan === "onetime") {
      paystack.newTransaction({
        key: "pk_test_6615d077735a133f04df732405a5adfb6d85850e",
        email: emailAddress.value,
        amount: oneTimeRentAmt * 100,
        currency: "GHS",

        onSuccess: (transaction) => {
          console.log(transaction);
          axios
            .post(
              "http://localhost:1738/payments/onetime?for_rent=true",
              {
                property_id: apiResponse?.pk,
                reference: transaction?.trxref,
                currency: "GHS",
                duration: duration.value,
                emailAddress: emailAddress.value,
                firstName: firstName.value,
                lastName: lastName.value,
                amount: oneTimeRentAmt,
              },
              {
                headers: {
                  Authorization: `Token ${Cookies.get("remarket")}`,
                },
              }
            )
            .then((response) => {
              console.log(response.data);
            });
        },
        onCancel: () => {
          // user closed popup
          console.log("Pop up closed");
        },
      });
    } else if (paymentPlan === "recurring") {
      paystack.newTransaction({
        key: "pk_test_6615d077735a133f04df732405a5adfb6d85850e",
        email: emailAddress.value,
        amount: apiResponse?.down_payment_amt * 100,
        currency: "GHS",

        onSuccess: (transaction) => {
          console.log(transaction);
          axios
            .post(
              "http://localhost:1738/payments/recurring?for_rent=true",
              {
                property_id: apiResponse?.pk,
                reference: transaction?.trxref,
                currency: "GHS",
                duration: duration.value,
                interval: billingInterval.value,
                emailAddress: emailAddress.value,
                firstName: firstName.value,
                lastName: lastName.value,
                amount: apiResponse?.down_payment_amt,
              },
              {
                headers: {
                  Authorization: `Token ${Cookies.get("remarket")}`,
                },
              }
            )
            .then((response) => {
              console.log(response.data);
            });
        },
        onCancel: () => {
          // user closed popup
          console.log("Pop up closed");
        },
      });
    }
  } else {
    if (paymentPlan === "onetime") {
      paystack.newTransaction({
        key: "pk_test_6615d077735a133f04df732405a5adfb6d85850e",
        email: emailAddress.value,
        amount: apiResponse?.price * 100,
        currency: "GHS",

        onSuccess: (transaction) => {
          console.log(transaction);
          axios
            .post(
              "http://localhost:1738/payments/onetime?for_rent=false",
              {
                property_id: apiResponse?.pk,
                reference: transaction?.trxref,
                currency: "GHS",
                emailAddress: emailAddress.value,
                firstName: firstName.value,
                lastName: lastName.value,
                amount: apiResponse?.price,
              },
              {
                headers: {
                  Authorization: `Token ${Cookies.get("remarket")}`,
                },
              }
            )
            .then((response) => {
              console.log(response.data);
            });
        },
        onCancel: () => {
          // user closed popup
          console.log("Pop up closed");
        },
      });
    } else if (paymentPlan === "recurring") {
      paystack.newTransaction({
        key: "pk_test_6615d077735a133f04df732405a5adfb6d85850e",
        email: emailAddress.value,
        amount: apiResponse?.down_payment_amt * 100,
        currency: "GHS",

        onSuccess: (transaction) => {
          console.log(transaction);
          axios
            .post(
              "http://localhost:1738/payments/recurring?for_rent=false",
              {
                property_id: apiResponse?.pk,
                reference: transaction?.trxref,
                currency: "GHS",
                emailAddress: emailAddress.value,
                firstName: firstName.value,
                lastName: lastName.value,
                mortgageDuration: mortgageDuration.value,
                amount: apiResponse?.down_payment_amt,
              },
              {
                headers: {
                  Authorization: `Token ${Cookies.get("remarket")}`,
                },
              }
            )
            .then((response) => {
              console.log(response.data);
            });
        },
        onCancel: () => {
          // user closed popup
          console.log("Pop up closed");
        },
      });
    }
  }
}

let authenticated = Boolean(Cookies.get("remarket"));

$(document).ready(function () {
  // replace dynamically generated elements with exisiting static ones
  $("#buyRentModal").on("hidden.bs.modal", function () {
    $("#paymentForm").html(`<div class="row mb-2">
    <div class="form-group col">
      <label for="first-name">First Name</label>
      <input
        readonly
        class="form-control"
        type="text"
        id="first-name"
      />
    </div>
    <div class="form-group col">
      <label for="last-name">Last Name</label>
      <input
        readonly
        class="form-control"
        type="text"
        id="last-name"
      />
    </div>
  </div>
  <div id="email-address-container" class="form-group mb-2">
    <label for="email">Email Address</label>
    <input
      readonly
      class="form-control"
      type="email"
      id="email-address"
      required
    />
  </div>`);
  });

  const header = document.querySelector(".header-nav");
  const userData = JSON.parse(localStorage.getItem("remarket"));
  if (authenticated) {
    const data = JSON.parse(localStorage.getItem("remarket"));
    header.innerHTML = "";
    header.innerHTML = `<li class="profile-name">
      <a href="http://localhost:1738/">Welcome ${data.first_name}</a>
    </li>`;
    header.innerHTML += `
   ${
     (userData?.user_type === OWNER || userData?.user_type === AGENT) &&
     !userData?.onboarded
       ? `<li>
       <a href="http://localhost:1738/onboarding/">Onboarding</a>
     </li>`
       : `
          <li>
            <a href="http://localhost:1738/listers/${userData?.pk}/properties">Listings</a>
          </li>
    `
   }
   <li>
      <a href="#"><i class="bi bi-bag" id="purchased"></i></a>
    </li>
    <li>
      <a href="#"><i class="bi bi-box-arrow-right" id="logout"></i></a>
    </li>
    `;

    const logout = document.querySelector("#logout");
    logout.addEventListener("click", function () {
      console.log("logging out");

      fetch("http://localhost:1738/logout", {
        method: "post",
        headers: {
          Authorization: `Token ${Cookies.get("remarket")}`,
        },
      }).then(async (res) => {
        if (res.ok) {
          alert("You have been successfully logged out");

          Cookies.remove("remarket");
          Cookies.remove("csrftoken");
          Cookies.remove("_xsrf");

          localStorage.removeItem("remarket");

          window.location.href = "http://localhost:1738"; //redirect to defualt page
        } else {
          let errorMessage = await res.json();
          if (typeof errorMessage === "object") {
            errorMessage = JSON.stringify(errorMessage);
          }
          alert(errorMessage || "Logging out failed, please try again");
        }
      });
    });

    const purchased = document.querySelector("#purchased");
    purchased.addEventListener("click", function () {
      //show modal  for purchase with table
      const purchasemodal = new bootstrap.Modal(
        document.getElementById("purchasedModal")
      );
      purchasemodal.show();
    });
  }

  // Event handler to listen for enter keyboard on the search and then trigger the click event on the search button
  $(".search-field").on("keypress", function (e) {
    if (e.which == 13) {
      // 13 is the keycode for the Enter key
      e.preventDefault(); // Prevent the default action (form submission)
      $(".search-button").click(); // Trigger the click event on the search button
    }
  });

  // $("#buyRentModal").on("hidden.bs.modal", () => {
  //   if ($("#duration").length) {
  //     $("#duration").remove();
  //   }
  //   if ($("#onetime").length || $("#recurring").length) {
  //     $("#onetime").remove();
  //     $("#recurring").remove();
  //   }
  // });

  // Make a GET request to your API endpoint
  $.get("/search/", function (data) {
    // console.log(data)
    // Parse the JSON response
    const apiResponse = data;

    // Get the "cards-section" div element by its ID
    const cardsSection = $("#cards-section");

    // Iterate over the "results" array in the API response
    apiResponse.results.forEach((result) => {
      // Create a new div element for each result
      const resultCard = $("<div>").addClass("result-card");

      // Create an image element and set its source
      const resultImage = $("<img>").attr("src", result.propertyimages[0]); // Assuming you want to use the first image

      // Create a div for result info
      const resultInfo = $("<div>").addClass("result-info");

      // Create an h2 element for property title
      const title = $("<h2>").text(result.name);

      // Create a paragraph for location, price, and type
      const infoParagraph = $("<p>").html(
        `Location: ${result.location_text ?? "Missing"}, ${
          result?.for_rent ? "Monthly Price:" : "Price:"
        } ${new Intl.NumberFormat("en-US", {
          style: "currency",
          currency: result?.currency || "GHS",
        }).format(result.price)} <br> Type: ${
          result.property_types
        }, Phone Number: ${result?.["lister_phone"]} <br> ${
          result?.for_rent
            ? `Minimum Allowed Rent Duration: ${convertMonths(
                result?.min_rent_duration
              )}`
            : ""
        } <br> ${
          result?.for_rent
            ? `Maximum Allowed Rent Duration: ${convertMonths(
                result?.max_rent_duration
              )}`
            : ""
        }`
      );

      // Create buttons div
      const buttonsDiv = $("<div>").addClass("buttons");

      // Create "Buy or Rent" button
      // Text is Buy if for_rent is false, else text is Rent
      const buyRentEditButton = (() => {
        if (
          (userData?.user_type === OWNER || userData?.user_type === AGENT) &&
          result?.lister_id === userData?.pk
        ) {
          return $("<a>")
            .text("Edit")
            .attr(
              "href",
              `/listers/${userData?.pk}/properties/${result?.pk}/edit`
            )
            .addClass("edit-button");
        } else if (userData?.user_type === RENTER) {
          return result?.for_rent
            ? $("<button>").addClass("buy-rent-button").text("Rent")
            : $("<button>").addClass("buy-rent-button").text("Buy");
        }
      })();

      // console.dir(buyRentEditButton);
      // Disable buttons if the user is not signed in
      !authenticated && buyRentEditButton?.attr("disabled", true);

      // Create "View More" button
      const viewMoreButton = $("<button>")
        .addClass("view-more-button")
        .text("View More");

      //set the pk to id , to be retrieved later and passed to buy and view more modals to get property detail
      buyRentEditButton?.attr("id", result.pk.toString());
      viewMoreButton.attr("id", result.pk.toString());

      // Append elements to resultInfo div
      resultInfo.append(title);
      resultInfo.append(infoParagraph);
      resultInfo.append(buttonsDiv);
      buttonsDiv.append(buyRentEditButton); // ! this button actually shows either buy/rent/edit depending on the condition met
      buttonsDiv.append(viewMoreButton);

      // Append image and resultInfo to resultCard
      resultCard.append(resultImage);
      resultCard.append(resultInfo);

      // Append resultCard to the "cards-section" div
      cardsSection.append(resultCard);
    });

    // view more button calls
    const RenterModal = document.querySelector(".renter-sign-in-button");
    // const RealtorRedirect = document.querySelector('.realtor-redirect');
    const purchasedModal = document.querySelector(".purhcased");
    // signUpChecker = document.querySelector(".form-check-input");
    const firstname = document.querySelector("#inputfirstname");
    const lastname = document.querySelector("#inputlastname");
    const email = document.querySelector("#exampleInputEmail1");
    const password = document.querySelector("#exampleInputPassword1");
    const signInBtn = document.querySelector("#sign_in");
    const signUpBtn = document.querySelector("#sign_up");
    const purchasemodal = document.querySelector("#purchasedModal");

    // add event listener for sign up  checker

    // signUpChecker.addEventListener("change", function () {
    //   if (signUpChecker.checked) {
    //     // enable the extra fields by removing the boot strap disabled attribute
    //     firstname.removeAttribute("disabled");
    //     lastname.removeAttribute("disabled");
    //   } else {
    //     firstname.setAttribute("disabled", "");
    //     lastname.setAttribute("disabled", "");
    //   }
    // });

    // Initialize a variable to track the checkbox state
    var checkboxChecked = false;

    // Reset field states when modal is hidden
    $("#signInModal").on("hidden.bs.modal", function () {
      $("#exampleCheck1[type='checkbox']").prop("checked", false);
      checkboxChecked = false; // Reset the variable
      updateFieldsState(); // Update field states
    });

    // Enable/disable fields based on checkbox state
    $("#exampleCheck1[type='checkbox']").change(function () {
      checkboxChecked = $(this).is(":checked");
      updateFieldsState(); // Update field states
    });

    // Prevent radio buttons from enabling/disabling fields if checkbox is not checked
    $("#agentRadio[type='radio']").change(function () {
      if (!checkboxChecked) {
        return false;
      }
    });
    $("#renterRadio[type='radio']").change(function () {
      if (!checkboxChecked) {
        return false;
      }
    });
    $("#ownerRadio[type='radio']").change(function () {
      if (!checkboxChecked) {
        return false;
      }
    });

    function updateFieldsState() {
      if (checkboxChecked) {
        $("#inputfirstname").prop("disabled", false);
        $("#inputlastname").prop("disabled", false);
        $("#inputphonenumber").prop("disabled", false);
        $("#sign_up").prop("disabled", false);
        $("#sign_in").prop("disabled", true);
      } else {
        $("#inputfirstname").prop("disabled", true);
        $("#inputlastname").prop("disabled", true);
        $("#inputphonenumber").prop("disabled", true);
        $("#sign_up").prop("disabled", true);
        $("#sign_in").prop("disabled", false);
      }
    }

    function showToast(message, success = true) {
      // Get the toast element

      const toast = document.getElementById("myToast");
      const toastMessageElement = document.querySelector(".toast-body");
      toastMessageElement.innerText = message;
      // Set the toast color based on success or failure
      toast.classList.remove("bg-success", "bg-danger");
      toast.classList.add(success ? "bg-success" : "bg-danger");

      // Create a new bootstrap.Toast instance
      const bsToast = new bootstrap.Toast(toast);

      // Show the toast
      bsToast.show();

      // Set the toast message
    }

    RenterModal?.addEventListener("click", function () {
      // Show the View More Modal for sign in
      const RenterAuthModal = new bootstrap.Modal(
        document.getElementById("signInModal")
      );
      RenterAuthModal.show();
      // grab form
      const form = document.querySelector(".authform");
      // Function to show a Bootstrap toast with a message

      form.addEventListener("submit", function (event) {
        // Prevent the default form submission
        event.preventDefault();
      });
      // event listener for login
      signInBtn.addEventListener("click", function (event) {
        // on successful sign in hide modal

        const radioButtons = Array.from(
          document.querySelectorAll('input[name="userType"')
        );
        const userType = radioButtons.find((radio) => radio.checked);

        const isFormValid = form.checkValidity();
        if (isFormValid) {
          $.post(
            "/login",
            {
              email: email.value,
              password: password.value,
              user_type: userType.value,
            },
            function (data) {
              const key = "remarket";
              const cookieString = `${key}=${data.token}`;
              localStorage.setItem("remarket", JSON.stringify(data));
              document.cookie = cookieString; // add  token cookie to dom , used later to authenticate  other requests
              header.innerHTML = "";
              header.innerHTML = `<li class = "profile-name"><a href = "#">Welcome ${data.first_name}<a/></li>`;
              header.innerHTML +=
                '<li><a href = "#"> <i class="bi bi-bag " id = "purchased"></i> </li> <li><a href = "#"><i class="bi bi-box-arrow-right" id = "logout" ></i><a/></li>';

              // toggle authenticated status
              authenticated = !authenticated;

              const logout = document.querySelector("#logout");
              logout.addEventListener("click", function () {
                console.log("logging out");

                fetch("http://localhost:1738/logout", {
                  method: "post",
                  headers: {
                    Authorization: `Token ${Cookies.get("remarket")}`,
                  },
                }).then(async (res) => {
                  if (res.ok) {
                    alert("You have been successfully logged out");

                    Cookies.remove("remarket");
                    Cookies.remove("csrftoken");
                    Cookies.remove("_xsrf");

                    localStorage.removeItem("remarket");

                    // toggle authenticated status
                    authenticated = !authenticated;

                    window.location.href = "http://localhost:1738"; //redirect to defualt page
                  } else {
                    let errorMessage = await res.json();
                    if (typeof errorMessage === "object") {
                      errorMessage = JSON.stringify(errorMessage);
                    }
                    alert(
                      errorMessage || "Logging out failed, please try again"
                    );
                  }
                });
              });

              const purchased = document.querySelector("#purchased");
              purchased.addEventListener("click", function () {
                //show modal  for purchase with table
                const purchasemodal = new bootstrap.Modal(
                  document.getElementById("purchasedModal")
                );
                purchasemodal.show();
              });

              form.reset(); //reset form
              RenterAuthModal.hide(); // hide form
              window.location.reload(true);
            }
          ).fail(function (jqXHR, textStatus, errorThrown) {
            // handle error
            if (jqXHR.status === 400) {
              showToast(jqXHR.responseText, false);
            }
          });
        }
      });

      // event listener for sign up
      signUpBtn.addEventListener("click", function (event) {
        // event.preventDefault();
        console.log("Submit sign up fired");
        const isFormValid = form.checkValidity();
        if (isFormValid) {
          const email = document.querySelector("#exampleInputEmail1");
          const firstName = document.querySelector("#inputfirstname");
          const lastName = document.querySelector("#inputlastname");
          const phoneNumber = document.querySelector("#inputphonenumber");
          const username = generateUsername(email.value);
          const password = document.querySelector("#exampleInputPassword1");

          const radioButtons = Array.from(
            document.querySelectorAll('input[name="userType"')
          );
          const userType = radioButtons.find((radio) => radio.checked);

          fetch("http://localhost:1738/register", {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: email.value,
              first_name: firstName.value,
              last_name: lastName.value,
              phone: phoneNumber.value,
              username: username,
              password: password.value,
              user_type: userType.value,
            }),
          }).then(async (res) => {
            if (res.ok) {
              showToast("Form submitted successful! Please sign in now.", true);
              form.reset(); //reset form
              firstName.setAttribute("disabled", true);
              lastName.setAttribute("disabled", true);
              phoneNumber.setAttribute("disabled", true);
              $("#sign_in").prop("disabled", false);
              $("#sign_up").prop("disabled", true);
            } else {
              let errorMessage = await res.json();
              if (typeof errorMessage === "object") {
                errorMessage = JSON.stringify(errorMessage);
              }
              showToast(
                errorMessage || "Form submission failed. Please try again.",
                false
              );
            }
          });
        }
      });
    });

    const viewMoreButtons = document.querySelectorAll(".view-more-button");
    const searchButtons = document.querySelectorAll(".search-button");
    const buyRentButtons = document.querySelectorAll(".buy-rent-button");

    viewMoreButtons.forEach((viewMoreButton) => {
      viewMoreButton.addEventListener("click", (event) =>
        viewMoreEventHandler(event, viewMoreButton)
      );
    });

    buyRentButtons.forEach((buyRentButton) => {
      buyRentButton.addEventListener("click", (event) =>
        buyOrRentEventHanlder(event, buyRentButton)
      );
    });
  });
});

// script with event listener  to get  listings based on parameters
$(document).ready(function () {
  const searchButton = document.querySelector(".search-button"); // get search button
  const resultDiv = document.querySelector("#cards-section"); // get listings  cards
  searchButton.addEventListener("click", function () {
    // const location = document.querySelector(".location-dropdown").value;
    // const price = document.querySelector(".price-dropdown").value;
    // const type = document.querySelector(".type-dropdown").value;
    const searchValue = document.querySelector(".search-field").value;
    query = `http://localhost:1738/search?search=${searchValue}`;
    // &location=${location}&type=${type}
    $.get(query, function (data) {
      console.log(data);
      //   // Parse the JSON response
      const apiResponse = data;
      // Get the "cards-section" div element by its ID
      const cardsSection = $("#cards-section");
      resultDiv.innerHTML = "";

      // Iterate over the "results" array in the API response
      apiResponse.results.forEach((result) => {
        // Create a new div element for each result
        const resultCard = $("<div>").addClass("result-card");

        // Create an image element and set its source
        const resultImage = $("<img>").attr("src", result.propertyimages[0]); // Assuming you want to use the first image

        // Create a div for result info
        const resultInfo = $("<div>").addClass("result-info");

        // Create an h2 element for property title
        const title = $("<h2>").text(result.name);

        // Create a paragraph for location, price, and type
        const infoParagraph = $("<p>").html(
          `Location: ${result.location_text ?? "Missing"}, ${
            result?.for_rent ? "Monthly Price:" : "Price:"
          } ${new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: result?.currency || "GHS",
          }).format(result.price)} <br> Type: ${
            result.property_types
          }, Phone Number: ${result?.["lister_phone"]} <br> ${
            result?.for_rent
              ? `Minimum Allowed Rent Duration: ${convertMonths(
                  result?.min_rent_duration
                )}`
              : ""
          } <br> ${
            result?.for_rent
              ? `Maximum Allowed Rent Duration: ${convertMonths(
                  result?.max_rent_duration
                )}`
              : ""
          }`
        );

        // Create buttons div
        const buttonsDiv = $("<div>").addClass("buttons");

        // Create "Buy or Rent" button
        // Text is Buy if for_rent is false, else text is Rent
        const buyRentButton = result?.for_rent
          ? $("<button>").addClass("buy-rent-button").text("Rent")
          : $("<button>").addClass("buy-rent-button").text("Buy");

        // Disable buttons if the user is not signed in
        !authenticated && buyRentButton.attr("disabled", true);

        // Create "View More" button
        const viewMoreButton = $("<button>")
          .addClass("view-more-button")
          .text("View More");

        //set the pk to id , to be retrieved later and passed to buy and view more modals to get property detail
        buyRentButton.attr("id", result.pk.toString());
        viewMoreButton.attr("id", result.pk.toString());
        // Append elements to resultInfo div
        resultInfo.append(title);
        resultInfo.append(infoParagraph);
        resultInfo.append(buttonsDiv);
        buttonsDiv.append(buyRentButton);
        buttonsDiv.append(viewMoreButton);

        // Append image and resultInfo to resultCard
        resultCard.append(resultImage);
        resultCard.append(resultInfo);

        // Append resultCard to the "cards-section" div
        cardsSection.append(resultCard);

        // view more button calls
        const viewMoreButtons = document.querySelectorAll(".view-more-button");
        const searchButtons = document.querySelectorAll(".search-button");
        const buyRentButtons = document.querySelectorAll(".buy-rent-button");

        viewMoreButtons.forEach((viewMoreButton) => {
          viewMoreButton.addEventListener("click", (event) =>
            viewMoreEventHandler(event, viewMoreButton)
          );
        });

        buyRentButtons.forEach((buyRentButton) => {
          buyRentButton.addEventListener("click", (event) =>
            buyOrRentEventHanlder(event, buyRentButton)
          );
        });
      });
    });
  });
});
