function getCookie(key) {
    // Split the document.cookie string into an array of cookies
    const cookies = document.cookie.split(';');
  
    // Iterate through the cookies to find the one with the specified key
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim(); // Remove leading/trailing spaces
      const cookieParts = cookie.split('=');
      
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
  const myCookieValue = getCookie('myCookieKey');
  
  if (myCookieValue !== null) {
    console.log(`Value of myCookieKey: ${myCookieValue}`);
  } else {
    console.log('Cookie not found or key does not exist.');
  }


  const paymentForm = document.getElementById('paymentForm');
  paymentForm.addEventListener("submit", payWithPaystack, false);
  
  function payWithPaystack(e) {
    e.preventDefault();
  
    let handler = PaystackPop.setup({
      key: 'pk_test_8eb3d442920820284fea0d6fcc245ebab8dfbf1b', // Replace with your public key
      email: document.getElementById("email-address").value,
      amount: document.getElementById("amount").value * 100,
      currency : 'GHS',
      ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
      // label: "Optional string that replaces customer email"
      onClose: function(){
        // alert('Window closed.');
      },
      callback: function(response){
        let message = 'Payment complete! Reference: ' + response.reference;
        // alert(message);
      }
    });
  
    handler.openIframe();
  }
  
$(document).ready(function() {

    // Make a GET request to your API endpoint
    $.get('/search/', function(data) {

      // console.log(data)
        // Parse the JSON response
        const apiResponse = data;

        // Get the "cards-section" div element by its ID
        const cardsSection = $('#cards-section');

        // Iterate over the "results" array in the API response
        apiResponse.results.forEach(result => {
            // Create a new div element for each result
            const resultCard = $('<div>').addClass('result-card');

            // Create an image element and set its source
            const resultImage = $('<img>').attr('src', result.propertyimages[0]); // Assuming you want to use the first image

            // Create a div for result info
            const resultInfo = $('<div>').addClass('result-info');

            // Create an h2 element for property title
            const title = $('<h2>').text(result.name);
            

            // Create a paragraph for location, price, and type
            const infoParagraph = $('<p>').text(`Location: ${result.location_text}, Price: ${result.currency}${result.price}, Type: ${result.property_types}`);

            // Create buttons div
            const buttonsDiv = $('<div>').addClass('buttons');

            // Create "Buy/Rent" button
            const buyRentButton = $('<button>').addClass('buy-rent-button').text('Buy/Rent');

            // Create "View More" button
            const viewMoreButton = $('<button>').addClass('view-more-button').text('View More');

            //set the pk to id , to be retrieved later and passed to buy and view more modals to get property detail
            buyRentButton.attr('id', (result.pk).toString())
            viewMoreButton.attr('id', (result.pk).toString())

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


        });

        // view more button calls
        const viewMoreButtons = document.querySelectorAll('.view-more-button'); 
        const searchButtons = document.querySelectorAll('.search-button');
        const buyRentButtons = document.querySelectorAll('.buy-rent-button');
        const RenterModal = document.querySelector('.renter-sign-in-button');
        // const RealtorRedirect = document.querySelector('.realtor-redirect');
        const purchasedModal = document.querySelector('.purhcased');
        signUpChecker = document.querySelector('.form-check-input');
        firstname = document.querySelector('#inputfirstname')
        lastname = document.querySelector('#inputlastname')
        email = document.querySelector('#exampleInputEmail1');
        password = document.querySelector('#exampleInputPassword1');
        signInBtn = document.querySelector('#sign_in');
        signUpBtn = document.querySelector('#sign_up');
        header = document.querySelector(".header-nav")
        purchasemodal = document.querySelector('#purchasedModal')



        // add event listener for sign up  checker 
        signUpChecker.addEventListener('change' , function () {
            if(signUpChecker.checked) {
                // enable the extra fields by removing the boot strap disabled attribute 
                firstname.removeAttribute('disabled')
                lastname.removeAttribute('disabled') 
            }
            else{
                firstname.setAttribute('disabled', '');
                lastname.setAttribute('disabled', '');

            }   
            
        })

        RenterModal.addEventListener('click', function() {
            // Show the View More Modal for sign in
            const RenterAuthModal = new bootstrap.Modal(document.getElementById('signInModal'));
            RenterAuthModal.show();
            // grab form
            const form = document.querySelector('.authform');
            form.addEventListener('submit', function (event) {
                // Prevent the default form submission
                event.preventDefault();
                // event listener for login 
                signInBtn.addEventListener('click', function() {
                    // on successful sign in hide modal
                    $.post('/login', {
                    username:  email.value,
                    password: password.value
                    }, function (data) {

                        const key = ' remarket'
                        const cookieString = `${key}=${data}`;
                        document.cookie = cookieString; // add  token cookie to dom , used later to authenticate  other requests
                        header.innerHTML = ''
                        header.innerHTML = `<li class = "profile-name"><a href = "#">Welcome ${data.first_name}<a/></li>` 
                        header.innerHTML += '<li><a href = "#"> <i class="bi bi-bag " id = "purchased"></i> </li> <li><a href = "#"><i class="bi bi-box-arrow-right" id = "logout" ></i><a/></li>'
                        const logout = document.querySelector('#logout');
                        logout.addEventListener('click', function(){
                            console.log('logging out')
                            document.cookie =  "" // flush cookies on logout 
                            window.location.href = 'http://localhost:1738'//redirect to defualt page
                        });

                        const purchased = document.querySelector('#purchased');
                        purchased.addEventListener('click', function(){
                            //show modal  for purchase with table 
                            const purchasemodal = new bootstrap.Modal(document.getElementById('purchasedModal'));
                            purchasemodal.show()
                        });
                })
                    form.reset() //reset form
                    RenterAuthModal.hide(); // hide form

                });

                // event listener for sign up  
                signUpBtn.addEventListener('click', function() {



                    // {
                    //     "username": "juniorigs",
                    //     "password": "1234567",
                    //     "email": "renter@g.com",
                    //     "first_name": "Kofi",
                    //     "last_name": "mensah",
                    //     "user_type":2
                    // }
                    form.reset() //reset form
                    // on successful sign up  in hide modal
                    RenterAuthModal.hide();
                });
                ;});

        });


        viewMoreButtons.forEach(viewMoreButton => {
          viewMoreButton.addEventListener('click', function() {
            const pk = parseInt(viewMoreButton.id)//grab the pk of the property  through element id 
            $.get(`/api/listing/${pk}/`,function(data) {
                const apiResponse = data
                console.log(apiResponse)
                pictures = document.getElementById('carousel-inner')
                property_title = document.getElementById('title')
                main_details = document.getElementById('main_details')
                other_details = document.getElementById('other_details')

                property_title.innerHTML = ''
                main_details.innerHTML= ''
                other_details.innerHTML = ''
                pictures.innerHTML = ''

                property_title.innerHTML = data.name
                main_details.innerHTML = `Location: ${data.location_text}, Price: ${data.currency} ${data.price}, Type: ${data.property_types}`
                other_details.innerHTML = ` Description : ${data.description}`

                data.propertyimages.forEach(propertyimage => {
                    pictures.innerHTML += `<div class="carousel-item active"><img src=${propertyimage} class="d-block w-100" alt="Gallery Image 1"></div>`

                })
                
                // update the values in the generic viewmoremodal   
                const viewMoreModal = new bootstrap.Modal(document.getElementById('viewMoreModal'));
                // Show the View More Modal
                viewMoreModal.show();
            })         
          });
      });


        buyRentButtons.forEach(buyRentButton => {
          buyRentButton.addEventListener('click', function() {

            const pk = parseInt(buyRentButton.id)//grab the pk of the property  through element id 
            $.get(`/api/listing/${pk}/`,function(data) {
                const apiResponse = data
                console.log(apiResponse)
                
            })
              // get the details  from api ; amount of the property in this case  
              // update the amount of the generic purchase template   
              // Show the update purchase  Modal
            const buyRentModal = new bootstrap.Modal(document.getElementById('buyRentModal'));
            buyRentModal.show();
          });
  });
    });
});


// script with event listener  to get  listings based on parameters
$(document).ready(function() {
  const searchButton = document.querySelector('.search-button'); // get search button 
  const resultDiv = document.querySelector('#cards-section'); // get listings  cards 
  searchButton.addEventListener('click', function() {
    const location = document.querySelector('.location-dropdown').value;
    const price = document.querySelector('.price-dropdown').value;
    const type = document.querySelector('.type-dropdown').value;
    const searchValue = document.querySelector('.search-field').value
    query = `http://localhost:1738/search?search=${searchValue}`
    // &location=${location}&type=${type}
    $.get(query, function(data) {

        console.log(data)
        //   // Parse the JSON response
          const apiResponse = data;
                      // Get the "cards-section" div element by its ID
          const cardsSection = $('#cards-section');
          resultDiv.innerHTML = ''
  
          // Iterate over the "results" array in the API response
          apiResponse.results.forEach(result => {
              // Create a new div element for each result
              const resultCard = $('<div>').addClass('result-card');
  
              // Create an image element and set its source
              const resultImage = $('<img>').attr('src', result.propertyimages[0]); // Assuming you want to use the first image
  
              // Create a div for result info
              const resultInfo = $('<div>').addClass('result-info');
  
              // Create an h2 element for property title
              const title = $('<h2>').text(result.name);
  
              // Create a paragraph for location, price, and type
              const infoParagraph = $('<p>').text(`Location: ${result.location_text}, Price: ${result.currency}${result.price}, Type: ${result.property_types}`);
  
              // Create buttons div
              const buttonsDiv = $('<div>').addClass('buttons');
  
              // Create "Buy/Rent" button
              const buyRentButton = $('<button>').addClass('buy-rent-button').text('Buy/Rent');
  
              // Create "View More" button
              const viewMoreButton = $('<button>').addClass('view-more-button').text('View More');
  
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
        const viewMoreButtons = document.querySelectorAll('.view-more-button'); 
        const searchButtons = document.querySelectorAll('.search-button');
        const buyRentButtons = document.querySelectorAll('.buy-rent-button');

        viewMoreButtons.forEach(viewMoreButton => {
          viewMoreButton.addEventListener('click', function() {
              // Show the View More Modal
              const viewMoreModal = new bootstrap.Modal(document.getElementById('viewMoreModal'));
              viewMoreModal.show();
          });
      });


        buyRentButtons.forEach(buyRentButton => {
          buyRentButton.addEventListener('click', function() {
              // Show the View More Modal
              const buyRentModal = new bootstrap.Modal(document.getElementById('buyRentModal'));
              buyRentModal.show();
          });
  });
    
  });
});
});
})

