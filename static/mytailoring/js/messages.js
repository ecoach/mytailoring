ecoach = {};

!function ($) {
    ecoach.messages =  {
        IFRAME_AUTO_HEIGHT_CONFIG: {
            heightCalculationOverrides: [{
                browser: 'mozilla',
                calculation: function (iframe, $iframeBody, options, browser) {
                    // since the jquery browser is passed in you can also check specific versions if desired
                    return iframe.contentDocument.documentElement.scrollHeight + options.heightOffset;
                }
            }]
        },

        initReady: function() {
            ecoach.messages.initTooltips();
            ecoach.messages.initPopover();
            ecoach.messages.initExternalLinks();
            ecoach.messages.initModal();
            ecoach.messages.initLogClickEvent();
            ecoach.messages.initTabs();
            ecoach.messages.initGetThingsDone();
            ecoach.messages.initAccordions();
            ecoach.messages.initPreventDefault();     
            ecoach.messages.resizeThumbnailContainer();
            ecoach.messages.initCarousel();
        },

        initLoad: function() {
            ecoach.messages.resizeThumbnailContainer();
        },

        resizeThumbnailContainer: function() {
            $(".thumbnail").each(function() {
                var thumbnail = this;
                var img = $(this).find("img");
                var imgRealWidth;
                $("<img/>") // Make in memory copy of image to avoid css issues
                    .attr("src", $(img).attr("src"))
                    .load(function() {
                        imgRealWidth = this.width; 
                        $(thumbnail).width(imgRealWidth); 
                    });
                
            });
        },

        initPreventDefault: function() {
            $(".prevent-default, a.clickable-icon").click(function(e) {
                e.preventDefault();
            });
        },

        initTooltips: function() {
            //initialize bootstrap tooltips
            $("#message-content [rel='tooltip']").tooltip().click(function(e) {
                if($(this).attr('href') == "#") {
                    e.preventDefault();
                }
            });
        },

        initPopover: function () {
            // initialize basic bootstrap popover with close button capability
            $("#message-content a[data-toggle=popover]").popover({
                title : function() {
                    if ($(this).attr("data-title")) {
                        return $(this).attr("data-title") + "<button type='button' class='close'>&times;</button>";
                    } else {
                        return false;
                    }
                },
                html : true
            //options could go here...
            }).click(function(e) {
                e.preventDefault();
                // create the log event
                var logCategory = "popover";
                var logAction = $(this).html();
                var logLabel = $(this).attr('data-title');
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });

            // enable close button on popover
            $(document).on('click', "#message-content .popover .close, #message-content .popover .close-trigger", function (e) {
                $("a[data-toggle=popover]").popover('hide');
            });
        },

        initExternalLinks: function () {
            // initialize basic bootstrap popover with close button capability
            $(".data-log-external").click(function(e){
                // create the log event
                var logCategory = "external-link";
                var logAction = $(this).attr('href');
                var logLabel = $(this).html();
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });
        },

        initModal: function() {
            // reload the iframe src on modal close if a modal contains an iframe. this ensures that the video (and its audio) will stop 
            $('.modal').on('show', function () {
                var modalVideo = $(this).find("iframe");
                // create the log event
                var logCategory = "modal";
                var logAction = "open";
                var logLabel = modalVideo.attr("src"); 
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });
            $('.modal').on('hidden', function () {
                var modalVideo = $(this).find("iframe");
                modalVideo.attr("src", modalVideo.attr("src")); 
                // create the log event
                var logCategory = "modal";
                var logAction = "close";
                var logLabel = modalVideo.attr("src"); 
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });
        },

        initLogClickEvent: function() {
            //log an event any time an element with attributes data-log-category and data-log-action is clicked. optionally may also have data-log-label, data-success-message (an element selector), data-success-modal (also an element selector)
            $("[data-log-category][data-log-action]").click(function(e) {
                var clickedElem = $(this);

                // clean this out of here
                var successMessageElem = $($(clickedElem).attr("data-success-message"));
                var successModalElem = $($(clickedElem).attr("data-success-modal"));
                if (successMessageElem.length > 0) {    
                    $(clickedElem).hide();
                }
                // log event
                var logCategory = $(this).attr("data-log-category");
                var logAction = $(this).attr("data-log-action");
                var logLabel = $(this).attr("data-log-label");
                var logValue = $(this).attr("data-log-value");
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);

                // intentionally did not put in a success callback. no need to bother user or slow down UI feedback if for some reason logging fails.
                if (successMessageElem.length > 0) { 
                    if($(successMessageElem).hasClass("fade")) {
                        $(successMessageElem).addClass("in");
                    } else {
                        $(successMessageElem).show();   
                    }
                }

                successModalElem.modal("show");
            });
        },

        initCarousel: function() {

            $('.carousel').carousel({
                interval: 5000
            });
            // apply click handlers to all a tags inside of accordion-group tags
            $(".carousel-control").click(function (e) {
                // create the log event
                var logCategory = "carousel";
                var logAction = $(this).attr('data-slide')
                var logLabel = false;
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });
        },

        initGetThingsDone: function() {
            $(".gtd_checkbox :checkbox").change(function (e) {
                // create the log event
                var logCategory = "get-things-done";
                if(this.checked)
                    var logAction = 'check';
                else
                    var logAction = 'uncheck';
                var logLabel = $(this).closest('.gtd_checkbox').nextAll('.gtd_text').first().text();
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });
        },

        initAccordions: function() {
            // apply click handlers to all a tags inside of accordion-group tags
            $(".accordion-group a").click(function (e) {
                // create the log event
                var logCategory = "accordion";
                if($(this).parentsUntil('.accordion-group').children('.accordion-body').hasClass('in'))
                    var logAction = 'closing'
                else
                    var logAction = 'opening'
                var logLabel = $(this).html();
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
            });
        },

        // if user refreshes page while on tab, they will stay on that tabs. also enables direct linking to a page's tab through use of url hash and GA tracking
        initTabs: function() {
            // Javascript to enable link to tab
            var url = document.location.toString();
            if (url.match('#')) {
                var tabLink = $('.nav-tabs a[href=#'+url.split('#')[1]+']');

                tabLink.tab('show');

                //reload any iframe content in that tab and size appropriately
                var tabContent = $($(tabLink).attr("data-target"));
                tabContent.find('iframe').attr( 'src', function ( i, val ) { return val; });
                tabContent.find('iframe').iframeAutoHeight(ecoach.messages.IFRAME_AUTO_HEIGHT_CONFIG);
            } 

            // Change hash for page-reload
            $('.nav-tabs a').on('shown', function (e) {
                window.location.hash = e.target.hash;
                // create the log event
                var logCategory = "tab-navigation";
                var logAction = $(this).attr("href");
                var logLabel = false;
                var logValue = false;
                var elog = {}
                if (logCategory)
                    elog.eventCategory = logCategory;
                if (logAction)
                    elog.eventAction = logAction;
                if (logLabel)
                    elog.eventLabel = logLabel;
                if (logValue)
                    elog.eventValue = logValue;
                logger.logEvent(false, elog);
                //GA doesn't send the hash by default, but we may want to treat tabs as separate logical pages for tracking purposes
                //logger.logEvent(true); // page view only

                var tabContent = $($(e.target).attr("data-target"));
                tabContent.find('iframe').attr( 'src', function ( i, val ) { return val; });
                tabContent.find('iframe').iframeAutoHeight(ecoach.messages.IFRAME_AUTO_HEIGHT_CONFIG);
            });
            $("a.tab-link").click(function() {
                console.log('cool');
                $(".nav-tabs " + "a[href=" + $(this).attr("href") + "]").tab('show');
                window.scrollTo(0, 0);
            });

            //hack. forces a resize event to be triggered "on shown" so that tab content elements are sized properly
            $(".nav-tabs li a").on("shown", function() {
                $(window).resize();
            });
        }
    }
}(window.jQuery);
