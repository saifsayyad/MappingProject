# MappingProject

This project will keep on checking
`https://mapping-test.fra1.digitaloceanspaces.com/data/list.json`,
and fetches Article list from that list it takes `article_id` and fetches Article details from `https://mapping-test.fra1.digitaloceanspaces.com/data/articles/article_id.json` this url,
If media is found in Article details section, Media info is fetched from
`https://mapping-test.fra1.digitaloceanspaces.com/data/media/article_id.json` this url.

All of this info is stored in `Article` model and printed for each article.

### Steps to start Application:

* Create python virtual env
* Activate virtual env 
* Run `pip install -r requirement.txt`
* Start application by running `python main.py`

### Optional Parameters

* `--history` : This is a boolean parameter, if passed `MappingPorject` application will use data stored in `data_dump` folder.
* `--interval` : This flag expects `int` value to be passed, this will decide refresh interval in __minute__.

#### How to use Optional Parameter
```shell
python main.py --history --interval 3
```

### Test Strategy:

* In `test.py` file two test cases are written
  * `test_doc` this test case demonstrates the basic behaviour of `Application`.
  * `test_new_doc` this test case demonstrates the behaviour when new document is hosted on `list API`.


### Future improvements:

* Writing more thorough test cases.
* Implementing advanced `caching` mechanism.
* Improving __Printing__ format.


-------------------------------------
> **_Time To Create:_**  It took around 12-14 hrs to complete this project.
>
-------------------------------------