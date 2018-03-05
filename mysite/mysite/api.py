# api.py

from wagtail.api.v2.router import WagtailAPIRouter
# from wagtail.wagtailimages.api.v2.endpoints import ImagesAPIEndpoint
# from wagtail.wagtaildocs.api.v2.endpoints import DocumentsAPIEndpoint

from home.endpoints import WebsimPagesAPIEndpoint, SimulationExamplesAPIEndpoint

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint('pages', WebsimPagesAPIEndpoint)
# api_router.register_endpoint('images', ImagesAPIEndpoint)
# api_router.register_endpoint('documents', DocumentsAPIEndpoint)
api_router.register_endpoint('simulationexamples', SimulationExamplesAPIEndpoint)
