
$(document).ready(function(){
    $(".RETAIL_90_MAIL_RATES_B_FIELD").hide($("#id_RETAIL_90_MAIL_RATES_B").val().substring(0,1) != "Y");
    $(".RETAIL_90_MAIL_RATES_G_FIELD").hide($("#id_RETAIL_90_MAIL_RATES_B").val().substring(0,1) != "Y");

    $("#id_RETAIL_90_MAIL_RATES_B").change(function(){
        $(".RETAIL_90_MAIL_RATES_B_FIELD").toggle($("#id_RETAIL_90_MAIL_RATES_B").val() != "N");
        });

    $("#id_RETAIL_90_MAIL_RATES_G").change(function(){
        $(".RETAIL_90_MAIL_RATES_G_FIELD").toggle($("#id_RETAIL_90_MAIL_RATES_G").val() != "N");
        });
});

const labels = Array.from(document.getElementById("cfd_form").querySelectorAll("label"));
var labelText = [];
var labelMap = {};

for (var count = 0; count < labels.length; count++){
    const item = labels[count];
    var text = $(item).text();
    text = text.slice(0, text.length - 1);

    labelText.push(text);
    labelMap[text] = item;
}

$("#field-search").autocomplete({
    source : labelText,
    select : function(event, ui){
        const selectedLabel = ui.item.label;
        const label = labelMap[selectedLabel];

        var fieldset = closestElem(label, 'fieldset'); 

        if (fieldset.classList.contains('collapsed')){ 

            var header = fieldset.querySelector('h2');
            if (!header.classList.contains('blank')){
                header.querySelector('a').click();
            }         
                    
        }

        label.scrollIntoView();
    }
})

$(".discount-field").attr({
    "min" : 0,
    "max" : 100
});

$(".datepicker").datepicker();

$(".input-copy").click(function(e){
    e.preventDefault();
    var elem = e.target;        
    var parent = elem.parentElement;    
    var inputField = document.getElementById(parent.dataset.target);

    var currentIndex = Number(parent.dataset.index);
    var fieldNameSuffix = inputField.name.split("-");
    fieldNameSuffix = fieldNameSuffix.slice(2, fieldNameSuffix.length);
    fieldNameSuffix = fieldNameSuffix.join("-");   

    while (true){            
        var nextFieldName = "form-" + String(currentIndex + 1) + "-" + fieldNameSuffix;
        var nextField = document.getElementsByName(nextFieldName)[0];

        if (nextField == undefined || nextField == null) {
            break
        }
        
        nextField.value = inputField.value;

        currentIndex += 1;
    }
    
})


$(".section-copy").click(function(e){
    e.preventDefault();

    var index = e.target.dataset.index;
    var fieldset = closestElem(e.target, 'fieldset');

    var inputs = fieldset.querySelectorAll('input');
    var selects = fieldset.querySelectorAll('select');
    
    var copySection = function(sourceIndex, nodeList, nodesPerRow){
        /** 
         * This function copies the value of the specified field to all 
         * other forms in the formset.
         * Here, a nodeMatrix is built with N rows and M columns where N is the 
         * number of fields in the fieldset and M is the number of forms in the 
         * formset or nodesPerRow.
         * The value at the chosen index for each row is copied to every other 
         * field in the same row.
        **/

        var nodeMatrix = [];

        nodeList = Array.from(nodeList);
        for (var count = 0; count < nodeList.length / nodesPerRow; count++){
            // 0 3
            // 3 6
            // 6 9
            nodeMatrix.push(nodeList.slice(count * nodesPerRow, (count + 1) * nodesPerRow));
        }

        for (var count = 0; count < nodeMatrix.length; count++){
            var currentItem = nodeMatrix[count];
            var value = currentItem[index].value;

            for (var i = 0; i < nodesPerRow; i++){
                if (i !== index){
                    currentItem[i].value = value;
                }
            }
        }
    }

    copySection(index, inputs, 3);
    copySection(index, selects, 3);
})

$("#submit-pending").click(function(e){
    $(".confirmation_flag").val(false);
})

$("#submit").click(function(e){
    $(".confirmation_flag").val(true);
})