   // Get modal element
   var modal = document.getElementById("myModal");
   var closeBtn = document.getElementsByClassName("close")[0];
   // Get close button in footer
   var closeFooterBtn = document.getElementById("closeBtn");

   // Listen for open click
   // modalBtn.addEventListener("click", openModal);
   // Listen for close click
   closeBtn.addEventListener("click", closeModal);
   closeFooterBtn.addEventListener("click", closeModal);
   window.addEventListener("click", outsideClick);

   function openStoreMapModal(storeId) {
        console.log("%c openModal for " + storeId, "background-color:orange;")

        // Do logic here to get a Google (?) map 
        // For this demo just put up a canned png of a google map 
        // for somewhere in Oregon City

        modal.style.display = "block";
   }

   // Function to close modal
   function closeModal() {
       modal.style.display = "none";
   }

   // Function to close modal if outside click
   function outsideClick(e) {
       if (e.target == modal) {
           modal.style.display = "none";
       }
   }