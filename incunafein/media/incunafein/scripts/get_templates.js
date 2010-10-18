django.jQuery(document).ready(function() {
    django.jQuery("#id_parent").blur(function() {
        django.jQuery.post("/admin/page/page/get_templates/",
            {'page_id' : django.jQuery("#id_parent").val() },
            function(data){

                var sel = django.jQuery("#id_template_key");
                sel.empty();
                for (var i=0; i<data.length; i++) {
                  sel.append('<option value="' + data[i].id + '">' + data[i].desc + '</option>');
                }
            }, "json");

    });

});

// Overload dismissRelatedLookupPopup to force the blur function on the id_parent field
var  dismissRelatedLookupPopup = (function() {
    var original_dismissRelatedLookupPopup = dismissRelatedLookupPopup;

        return function(win, chosenId) {
            var fieldid = windowname_to_id(win.name);
            original_dismissRelatedLookupPopup(win, chosenId);
            if (fieldid == 'id_parent')
            {
                django.jQuery("#id_parent").trigger("blur");
            }

        }

})();
