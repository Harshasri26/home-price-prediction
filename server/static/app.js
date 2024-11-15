$(document).ready(function() {
    // Fetch location names from the Flask API
    $.get("/api/location_names", function(data) {
        if (data.locations && data.locations.length > 0) {
            // Populate the dropdown with location options
            data.locations.forEach(function(location) {
                $('#uiLocations').append('<option value="' + location + '">' + location + '</option>');
            });
        } else {
            console.log("No locations found.");
        }
    });

    // Event handler for the 'Estimate Price' button click
    $('#estimatePriceButton').on('click', function() {
        var total_sqft = $('#uiSqft').val();
        var location = $('#uiLocations').val();
        var bhk = $("input[name='uiBHK']:checked").val();
        var bath = $("input[name='uiBathrooms']:checked").val();

        // Display a loading message until we get the result
        $('#uiEstimatedPrice span').text('Loading...');

        // Call API to get the predicted price
        $.post("/api/predict_home_price", {
            total_sqft: total_sqft,
            location: location,
            bhk: bhk,
            bath: bath
        }, function(response) {
            // After receiving the response, update the price
            if(response && response.estimated_price) {
                $('#uiEstimatedPrice span').text('₹' + response.estimated_price);
            } else {
                $('#uiEstimatedPrice span').text('Error: Price could not be determined');
            }
        }).fail(function(xhr, status, error) {
            console.log("Error: " + error);
            $('#uiEstimatedPrice span').text('Error: Could not fetch price');
        });
    });
});
