from online_users.models import OnlineUserActivity
from accounts.models import Account
from orders.models import Order


def admin_index_processors(request):
    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()

    total_users = (Account.objects.count())

    # Generating sales report
    ind_products = 0
    transactions = 0
    product_sales = {}
    order = Order.objects.all()
    for o in order:
        transactions += 1
        items = o.orderitem_set.all()
        
        for i in items:
            print(str(i.product))
            if str(i.product) not in product_sales:
                product_sales[str(i.product)] = i.quantity
            else:
                product_sales[str(i.product)] = product_sales[str(i.product)] + i.quantity      

    print((product_sales)) 

    # Find indv product sales
    for pv in product_sales.values():
        ind_products += int(pv)  
  

    print(ind_products)
    print(transactions)    
        
    context = {'online_users' : number_of_active_users, 
        'total_users' : total_users, 
        'ind_products' : ind_products, 
        'transactions' : transactions
    }
    return context