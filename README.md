# Web_Spider
### Abstract

- A web spider searching all internal links and download it's content

- We designed a simple model with the help of multi-threads techniques.

### File structure

- search_across_website\

  - WaitingList.py

    A class which combines python list, python set and threading. This controls that the pull in and pop out of task always happens in thread -safe condition

  - testing_method.py

    A pastiche on testing those method used in this project including simple example on 'urllib3', 'beautifulsoup' and so on.

  - web_crawler_methods.py 

    Including methods on get internal/external links of certain beautiful soup object, read only the contents with ignoring tags like 'style' or 'script', and save the content into a .txt name with using md5 to cipher the name of url

- utils\

  - clean_path : use to clean result path, this will avoid clean files like *.py
  - md5_transfer : a md5 transfer method

- spidering_simple.py

  This is the version without using self-defined class (WaitingList) and threading, this may work for small task thanks to the confinement of depth in recursion.

- **spidering_with_thread.py**

  Here we use self-defined class and threading techniques to boost up the speed and safety of web crawling. You may wants to use/modify this in your own task

### Example

- You may wants to change the following parameters of **spidering_with_thread.py**, then run and see the results

  - save_path : where results should be saved
  - test times : how many pages you try to read
  - root: the page to start with 

- This is my result on requiring 100000 pages from one single root.

  ![image](https://github.com/MoonKuma/Web_Spider/blob/master/refer/result_of_100000.png)

  Well, 90% comes back and this only takes around 4 hours.

  Adding more works and running in a better web condition are sure to be of help

### Results

- Results are saved in a patten of Json string includes the url and contents of that url
- You may do whatever you want with the results like training a LSTM-RNN model, but please do not use this method in evil way.

### Requirement

- If you are using Python3 + Anaconda then nothing need to be installed

- Otherwise, those following packages are necessary

  ```
  BeautifulSoup -> 4.6.0
  urllib3 -> 1.24.1
  ```

- No, you could not use this on Python2, they do not allow Semaphore (of threading) to try acquire a key blocked with time limit.   

### Much thanks to https://zh.moegir.org !!~

 



