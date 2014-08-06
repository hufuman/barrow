Design
======

Web Page Classification
-----------------------

There are two basic types of web pages:

    * Standard HTML with full data available (We name it **standard page**)
    * HTML page but with ajax data loading (We name it **ajax page**)


And with standard page we can find two kinds of page data:

    * Content page (We name it **content page**)
    * List page for content ( We name it **list page**)

Also, there are two ways to load ajax pages:

    * Direct HTML transfer (We name it **html ajax page**)
    * Serialized data transfer, like JSON or XML (We name it **serialized ajax page**)

So, with this in mind, we should define spider rules according to following page types:

    * Content Page
    * List Page
    * HTML AJAX Page
    * Serialized AJAX Page


Following Spider
----------------

When we come across **list page**, there will be many pages of data, and we want to scrap the following data.

So there should be a way to define the **next url** to scrap from.

However besides the traditional query string parameter (like *page*), many other ways are taken depending on website developers.

So, we define two ways to calculate next url:

    * Standard query string parameter formation
    * Customized python function that returns next url, called by spider

