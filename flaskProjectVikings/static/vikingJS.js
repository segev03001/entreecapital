let aaa;
$.ajax({
  type: "POST",
  url: "https:///C:/Users/SEGEV/Desktop/entree%20capital/fronted/getdata/getData.py",
  data: { param: aaa}
}).done(function( o ) {
   console.log(aaa)
});