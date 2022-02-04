from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        # return result.getvalue()
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# <!doctype html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport"
#           content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
#     <meta http-equiv="X-UA-Compatible" content="ie=edge">
#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
#     <title>Invoice</title>
#
# </head>
# <body>
# {% block body %}
# <div>
#     <p>{{buyer}}</p>
# </div>
# <div style="display:flex;margin: 0 auto; float:left;">
#     <div>
#         <table>
#             <th>Product</th>
#             <tbody>
#                 {% for product in products %}
#                 <tr style="color:blue; ">
#                     <td>{{product.product_title}}</td>
#                 </tr>
#                 {% endfor %}
#             </tbody>
#         </table>
#     </div>
#     <div>
#         <table>
#             <th>Quantity</th>
#             <tbody>
#                 {% for quantity in quantities %}
#                 <tr style="color:blue; ">
#                     <td>{{quantity}}</td>
#                 </tr>
#                 {% endfor %}
#             </tbody>
#         </table>
#     </div>
#     <div>
#         <table>
#             <th>Price</th>
#             <tbody>
#                 {% for price in discounts %}
#                 <tr style="color:blue; ">
#                     <td>$ {{price}}</td>
#                 </tr>
#                 {% endfor %}
#             </tbody>
#         </table>
#     </div>
# </div>
# {% endblock %}
# </body>