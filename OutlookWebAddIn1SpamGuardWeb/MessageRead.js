'use strict';

(function () {

    Office.onReady(function () {
        // Office is ready
        $(document).ready(function () {
            // The document is ready
            loadItemProps(Office.context.mailbox.item);
        });
    });

    function loadItemProps(item) {
        // Write message property values to the task pane
        $('#item-id').text(item.itemId);
        $('#item-subject').text(item.subject);
        $('#item-internetMessageId').text(item.internetMessageId);
        $('#item-from').html(item.from.displayName + " &lt;" + item.from.emailAddress + "&gt;");
        $('#checkboxLabel').text("J'accepte la condition de confidentialité");
        $('#submit-btn').text("Soumettre");
    }

    // Dynamically setting the label text
    document.getElementById('checkboxLabel').innerText = "I agree to the terms of privacy.";

    function submitForm() {
        var checkbox = document.getElementById('agreeCheckbox');
        if (checkbox.checked) {
            console.log("Checkbox is checked - form can be submitted.");
            // Proceed with form submission or other actions
        } else {
            console.log("Checkbox is not checked - cannot submit the form.");
            alert("You must agree to the terms of privacy before proceeding.");
        }
}

})();


//(function () {
//  "use strict";

//  var messageBanner;

//  // La fonction d'initialisation Office doit être exécutée chaque fois qu'une nouvelle page est chargée.
//  Office.initialize = function (reason) {
//    $(document).ready(function () {
//      var element = document.querySelector('.MessageBanner');
//      messageBanner = new components.MessageBanner(element);
//      messageBanner.hideBanner();
//      loadProps();
//    });
//  };

//  // Prend un tableau d'objets AttachmentDetails, puis crée une liste de noms de pièces jointes séparés par un saut de ligne.
//  function buildAttachmentsString(attachments) {
//    if (attachments && attachments.length > 0) {
//      var returnString = "";
      
//      for (var i = 0; i < attachments.length; i++) {
//        if (i > 0) {
//          returnString = returnString + "<br/>";
//        }
//        returnString = returnString + attachments[i].name;
//      }

//      return returnString;
//    }

//    return "None";
//  }

//  // Met en forme un objet EmailAddressDetails en tant que
//  // GivenName Surname <emailaddress>
//  function buildEmailAddressString(address) {
//    return address.displayName + " &lt;" + address.emailAddress + "&gt;";
//  }

//  // Prend un tableau d'objets EmailAddressDetails, puis
//  // crée une liste de chaînes mises en forme, séparées par un saut de ligne
//  function buildEmailAddressesString(addresses) {
//    if (addresses && addresses.length > 0) {
//      var returnString = "";

//      for (var i = 0; i < addresses.length; i++) {
//        if (i > 0) {
//          returnString = returnString + "<br/>";
//        }
//        returnString = returnString + buildEmailAddressString(addresses[i]);
//      }

//      return returnString;
//    }

//    return "None";
//  }

//  // Charge les propriétés à partir de l'objet de base Item, puis charge les
//  // propriétés spécifiques au message.
//  function loadProps() {
//    var item = Office.context.mailbox.item;

//    $('#dateTimeCreated').text(item.dateTimeCreated.toLocaleString());
//    $('#dateTimeModified').text(item.dateTimeModified.toLocaleString());
//    $('#itemClass').text(item.itemClass);
//    $('#itemId').text(item.itemId);
//    $('#itemType').text(item.itemType);

//    $('#message-props').show();

//    $('#attachments').html(buildAttachmentsString(item.attachments));
//    $('#cc').html(buildEmailAddressesString(item.cc));
//    $('#conversationId').text(item.conversationId);
//    $('#from').html(buildEmailAddressString(item.from));
//    $('#internetMessageId').text(item.internetMessageId);
//    $('#normalizedSubject').text(item.normalizedSubject);
//    $('#sender').html(buildEmailAddressString(item.sender));
//    $('#subject').text(item.subject);
//    $('#to').html(buildEmailAddressesString(item.to));
//  }

//  // Fonction d'assistance pour afficher les notifications
//  function showNotification(header, content) {
//    $("#notificationHeader").text(header);
//    $("#notificationBody").text(content);
//    messageBanner.showBanner();
//    messageBanner.toggleExpansion();
//  }
//})();