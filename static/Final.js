
let Review_html = '  <form id="submit_review" name ="submit_review" > <label for="Rating">Rating</label>\
<select id="Rating" name="Rating" class="form-control">\
                            <option value="1">1</option>\
                            <option value="2">2</option>\
                            <option value="3">3</option>\
                            <option value="4">4</option>\
                            <option value="5">5</option>\
                        </select>\
                </br>\
                    <label>Comment Here</label>\
                    <input type="text" id="Review" name="Review" placeholder="Submit your Feedback Here"></input>\
                    <br>\
                    <br>\
                    <a href="#" onclick = my_func()>Submit Review  </a>\
                </form>'

  let table_start =        '<br><div class="card-header">\
                            <h1><b>Book Reviews</b></h1><br>\
                            <table id="myTable">\
                            <tr>\
                            <th><b>Username</b></th>\
                            <th><b>Rating</b></th>\
                            <th><b>Review</b></th>\
                            </tr>';
  let table_end  = '</table>';
 
   function my_func(){
          // console.log('hai')
          const submit_request = new XMLHttpRequest();
          submit_request.open('POST', '/api/submit_review');
          const Rating = document.querySelector('#Rating').value
          const Review = document.querySelector('#Review').value
          const ISBN   = document.querySelector('#ISBN').value
          console.log(ISBN)
          // console.log('hai')

          // Callback function for when request completes
          submit_request.onload = () => {
              console.log('hai-1')
              // Extract JSON data from request
              const data = JSON.parse(submit_request.responseText);
              console.log(data)
              console.log('hai-2')
              // Update the result div
              document.querySelector('#replace1').innerHTML = '<br>'+'<br>'+'<br>'+'<div class ="card-header">'+data.Result+'</div>';
             
          }

          // Add data to send with request
          const review_data = new FormData();
          review_data.append('rating', Rating);
          review_data.append('review', Review);
          review_data.append('ISBN',ISBN);
          // Send request
          submit_request.send(review_data);
          return false;

   }
  


    function showDiv(parameter){

    console.log(parameter.getAttribute('name'));
    const bookrequest = new XMLHttpRequest();
    const isbn_input = parameter.getAttribute('name');
    let output       = "<br><h2>Book Details :</h2> <br> "
    let review_form  = "<br><h2>Review Here</h2> <br>"
    bookrequest.open('POST','/api/book_details');
    // Callback function for when request completes
    bookrequest.onload = () => {
          // console.log(bookrequest.responseText);
         // Extract JSON data from request
        const data_retrieved = JSON.parse(bookrequest.responseText);
        output += '<div class = "card-header">'+"<h5> ISBN : "+data_retrieved.ISBN+"<br> Title : "+data_retrieved.Title+"<br> Year : "+data_retrieved.Year+"<br> Author :"+data_retrieved.Author+"</h5>"+'</div>';
        
        
        if (isNaN(data_retrieved.Rating)){
            console.log('yesssss opened')
            review_form += '<div class = "card-header">'+Review_html+'<input type="hidden" id="ISBN" name="ISBN" value='+isbn_input+'>'+'</div>' //review_html is form written on the top
        }else{
        review_form  =  '<br><h2>Your Review :</h2> <br>'+'<div class = "card-header">'+" <br>"+"Rating :  "+data_retrieved.Rating +"<br> Review :"+data_retrieved.Review+'</div>'
        }
        var message = "<h2>Reviews</h2> <br>";

        if (!data_retrieved.Review){
            message += "No Reviews Yet"
            console.log("hai")

        }
        else{
          document.getElementById("demo").innerHTML =  table_start;
        
        
          console.log(data_retrieved.Reviews.reviews)
          data_retrieved.Reviews.reviews.forEach(myFunction);
function myFunction(item, index) {
  var table = document.getElementById("myTable");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = item.username;
  cell2.innerHTML = item.rating;
  cell3.innerHTML = item.review;
}
        }
        document.getElementById("demo").innerHTML +=  table_end;


        // console.log(output)
        document.querySelector('#replace1').innerHTML= review_form;
        document.querySelector('#replace').innerHTML = output;

   

      }

  // Add data_retrieved to send with request
    const data_book = new FormData();
    data_book.append('isbn_input',isbn_input);
    // data_book.append('username',username);
    // Send request
    bookrequest.send(data_book);
    return false;

    // ShowReview(ISBN);


    }


    document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#search-form').onsubmit = () => {

    // Initialize new request
    const request = new XMLHttpRequest();
    const search_input = document.querySelector('#search_input').value;

    request.open('POST','/api/search');

 


    // Callback function for when request completes
    request.onload = () => {


      

        // Extract JSON data from request
        const data = JSON.parse(request.responseText);

        // Update the result div
        let data_fetched = "<br> <h2>Search Results</h2> <br>";
        if (data.success) {
          var j;
          for(j = 0;j<data.books_1.length;j++){
          // data_fetched +=  '<a href="#" onClick="showDiv('+data.books_1[j].ISBN +');">'+ data.books_1[j].ISBN + " Title :"+ data.books_1[j].Title+"  Year : "+data.books_1[j].Year+"  Author : "+data.books_1[j].Author+ '</a>'
          data_fetched += '<div class="card">'+Strings.create('<div class="card-header">{Title} </div> <div class="card-body"> <ul>{ISBN}</ul><ul>{Author}</ul><ul>{Year}</ul> </div>',{Title:data.books_1[j].Title,ISBN:data.books_1[j].ISBN,Author:data.books_1[j].Author,Year:data.books_1[j].Year})
          data_fetched += '<div class="card-footer">  <button class="btn btn-success" name='+data.books_1[j].ISBN+' onclick = showDiv(this)>View Book  </button></div> </div><br>'
          // console.log('<div class="card-footer">  <a href="#" onclick = showDiv('+data.books_1[j].ISBN+':'+data.books_1[j].Title+':'+data.books_1[j].Year+':'+data.books_1[j].Author+')>View Book  </a></div>')
          }
          document.querySelector('#search_result').innerHTML= data_fetched;
        }
        else {
          document.querySelector('#search_result').innerHTML=  'There was an error.'  
        }
    }




    // Add data to send with request
    const data = new FormData();
    data.append('search_input',search_input);


    // Send request
    request.send(data);
    return false;
};

});

var Strings = {
        create : (function() {
                var regexp = /{([^{]+)}/g;

                return function(str, o) {
                     return str.replace(regexp, function(ignore, key){
                           return (key = o[key]) == null ? '' : key;
                     });
                }
        })()
};


