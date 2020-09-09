    #EXAMPLE FLIGHTPATHS FOR JSONS

    # routine = {
    #     "url": "https://www.glassdoor.com/Overview/Working-at-UniGroup-EI_IE3422.11,19.htm",
    #     "flightpath": {
    #         "jobs": {
    #             "path": "//script[@type='application/ld+json']",
    #             TRANSFORM_parseJSONfromScript: {
    #                 "jsonPath": ["ratingValue"]
    #             }
    #         }
    #     },
    # }
    # routine = {
    #     "url": "https://de.indeed.com/cmp/Getyourguide", #model URL
    #     "flightpath": {
    #         "bio": {
    #             "path": "//script[contains(text(), 'window._initialData=JSON.parse(')]",
    #             TRANSFORM_parseJSONfromScript: {
    #                 "head": "window._initialData=JSON.parse('",
    #                 "tail": "');",
    #                 "id_company": ["topLocationsAndJobsStory", "companyName"],
    #                 "id_lessText": ["aboutStory", "aboutDescription", "lessText"]
    #             },
    #         }
    #     }
    # }
#     routine = {
#     "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
#     "flightpath": {
#         "header": "//*[@class='page-header']",
#         "jobs": [{
#             "iterate": "//div[@class='job']",
#             "title": ".//h4[@class='title']",
#             "description": ".//h4[@class='description']",
#             "dateposted": ".//div[@data-element-type='date']",
#             "salary": "//h3[@id='salary-query']",
#         }]
#     },
# }
