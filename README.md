### Pre requisites
Python 3.7 installed

[generic-shop-api](https://github.com/iagolivino92/generic-shop-api "generic-shop-api project") project running

### How to install
Just clone the project or donwload and extract the .zip file.

Open the terminal in the cloned/extracted folder (root) and run the following commands:

`python3.7 pip3 install -r requirements.txt`

`python3.7 main.py`

After executing the commands with success, just open your browser and go to the url:

`http://generic-shop.com:5000`
  
  
### How to use
Every time the [generic-shop-api](https://github.com/iagolivino92/generic-shop-api "generic-shop-api") project is executed, it will try to create the local admin instance if it does not exist.
- ##### First login

  To login with admin privilegies and start to use (creating new shops, users, employees, etc.) just go to the url:
  ###### Shop Portal
  **http://generic-shop.com:5000/login?shop=1** 
	
   ###### Credentials:
  `user: admin@local`
  `pass: localadministrator`
  ###### Employee Portal
  **http://employee.generic-shop.com:5000/login?shop=1** 
	
   ###### Credentials:
  `user: emp@local`
  `pass: 12345678`

- ##### What you can do as administrator (admin) - Shop Portal
	- Add/remove user (all roles)
	- Edit any user
	- Add/remove employee (for any shop)
	- Create entry (Join Request) to invite new user
	- Accept/Decline Join Requests (from invited users)
	- Create/remove shops
	- See/Update sales details for any user
	- See your sales and add new ones
	- Create sales reports for any user (this feature is not available for now)
	- See and update all your details (this feature is not available for now)

- ##### What you can do as manager (mgr) - Shop Portal
	- Edit/remove user (mgr or emp)
	- Add/remove employee (for current shop)
	- Create entry (Join Request) to invite new user
	- Accept/Decline Join Requests (from invited users)
	- See/Update sale details for users in the same shop
	- See your sales and add new ones
	- Create sales reports (date based)
	- See and update some of your details (this feature is not available for now)

- ##### What you can do as viewer (read) - Shop Portal
	- See employees details in the same shop
	- See your sales and add new ones
	- Create sales reports (date based)
	- See and update some of your details (this feature is not available for now)

- ##### What you can do as employee (emp) - Employee Portal
	- See your sales and add new ones
	- Create sales reports (date based)
	- See and update some of your details (this feature is not available for now)
