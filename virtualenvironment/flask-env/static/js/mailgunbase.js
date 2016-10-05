
$(document).ready(function(){
	$("#selectEvents li").on('click',function(){   
    var _this = $(this);        
    $("#selectEvents button.btn_text").text(_this.text());      
	});

	$('#btnunsubscribe').click(function(){
		
		$("#data_form").ajaxForm({
			/*url: '/unsubscribe',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});

	$('#btncreatecampaign').on('click',function(){
		
		$("#data_form2").ajaxForm({
			/*url: '/createCampaign',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	

	$('#btndeletecampaign').on('click',function(){
		
		$("#data_form").ajaxForm({
			/*url: '/deleteCampaign',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	

	$('#btnsendsingle').on('click',function(){
		$("#data_form").ajaxForm({
			/*url: '/sendEmailWithHtml',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	

	$('#btnsendsinglePDate').on('click',function(){
		
		$("#data_form").ajaxForm({
			/*url: '/sendEmailWithHtmlPDate',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	

	$('#btnsendscamapign').on('click',function(){
		
		$("#data_form").ajaxForm({
			/*url: '/sendCampWithHtml',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	

	$('#btnsendscampaignPDate').on('click',function(){
		
		$("#data_form").ajaxForm({
			/*url: '/sendCampWithHtmlPDate',
			data: $('form').serialize(),
			type: 'POST',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	

	$('#btnanalytics').on('click',function(){
		
		$("#data_form").ajaxForm({
			/*url: '/analyticsmain',
			data: $('form').serialize(),
			type: 'GET',*/
			dataType: 'json',
			success: function(response){
				$('#dummytest').append(response.message);
			},
			error: function(error){
				console.log(error);
			}
		});
	});	
});
