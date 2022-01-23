function callModel(){
  //gettting and setting question value
  var ques = document.getElementById("question").value;
  localStorage.setItem("quesValue", ques);

  // call backend and fetch json response


  // call pagerank google app script
  // make you own api key as "key" and "cx" as identifier of the Programmable Search Engine. 
  $.ajax({
    type: 'GET',
    url : "https://customsearch.googleapis.com/customsearch/v1?key=AIzaSyCnKtYHT7_j6j6Cs0_eVELcQ0Nbl-8DcoA&q=" + ques + "&cx=db7ef7bbe24c634da&num=5",
    // data: {'question' : ques},
    dataType: 'json',
    success: function(response){
      var parsed_data = JSON.stringify(response);
      parse = JSON.parse(parsed_data);

      var search_result_list = parse["items"]

      var search_result_injson = {"items" : search_result_list}

      /// qna data in dict
      localStorage.setItem("pr_search_result_data", JSON.stringify(search_result_injson));
      console.log(search_result_injson)
    },
    error: function(jqXHR, textStatus, errorThrown){
      alert("The following error occured: "+ textStatus, errorThrown, jqXHR);
    }
  });


  ///////// CALLING FAQ - {depricated}
  // var faqurl = "http://127.0.0.1:5001/answer/" + ques;
  // var xhttp = new XMLHttpRequest();
  // xhttp.onreadystatechange = function() {
  //   if (this.readyState == 4 && this.status == 200) {
  //     var faqdata = JSON.parse(this.responseText);
  //     /// faq data in dict
  //     localStorage.setItem("faqdata", faqdata.faq);
  //   }
  // };
  // xhttp.open("GET", faqurl, true);
  // xhttp.send();

///////// CALLING FAQ
  $.ajax({
    type: 'POST',
    url : "http://localhost:5001/faqanswer",
    data: {'question' : ques},
    dataType: 'json',
    success: function(response){
      var parsed_data = JSON.stringify(response);
      parse = JSON.parse(parsed_data);

      localStorage.setItem("faqdata", JSON.stringify(parse));
      console.log("faqdata  --> " + JSON.stringify(parse))

      // if(parse["retrieved_answer"]=='NONE' || parse["retrieved_question"]=='NONE'){
      //   localStorage.setItem("faqdata", parse.faq);
      //   localStorage.setItem("faq_retrieved_answer", parse.retrieved_answer);
      //   localStorage.setItem("faq_retrieved_question", parse.retrieved_question);
      // }
    },
    error: function(jqXHR, textStatus, errorThrown){
      alert("The following error occured: "+ textStatus, errorThrown, jqXHR);
    }
  });


  ///////// CALLING QNA RANKING
  $.ajax({
    type: 'POST',
    url : "http://localhost:5000/search",
    data: {'question' : ques},
    dataType: 'json',
    success: function(response){
      var parsed_data = JSON.stringify(response);
      parse = JSON.parse(parsed_data);

      var idx=5
      if(parse["0"]=='BITS Pilani')
       idx=1

      var ans;
      if(idx==1)
      {
        ans = {
          0: parse["0"],
          1: parse["1"],
        }
      }
      else
      {
        ans = {
          0: parse["0"],
          1: parse["1"],
          2: parse["2"],
          3: parse["3"],
          4: parse["4"],
          5: parse["5"]
        }
      }   
      /// qna data in dict
      localStorage.setItem("qnaindex", idx);
      localStorage.setItem("qnarankingdata", JSON.stringify(ans));
      console.log("qnarankingdata ---> " + JSON.stringify(ans))
      loadFunction();
    },
    error: function(jqXHR, textStatus, errorThrown){
      alert("The following error occured: "+ textStatus, errorThrown, jqXHR);
    }
  });

}

function loadFunction(){
  window.alert("Search Result found!!!!");
  location.replace("serp.html")
}