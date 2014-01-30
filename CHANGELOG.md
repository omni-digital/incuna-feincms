
= Changelog

== v1.1.0

* Add changelog based on git commit history.
* Use model._mptt_meta rather than model.__meta.
  django-mptt  >= 0.4.0 moved the mptt options from model._mptt_meta
  to model.__meta.

== v1.0.2

* Correct typo models -> model; Pep8 fixes

== v1.0.1

* Add the current navigation level to the context.

== v1.0.0

* Remove deprecated django.conf.urls.defaults import.

== v0.16.6

* Add partially complete changelog. Goes toward #2.
* Use `MediaFileForeignKey` for `VideoSectionContent`.
* Drop legacy support hacks.
* Remove django 1.3 support.
* Whit espace.
* Code standards.
* Import order.

== v0.16.5

* FeinCMS v1.7 compatibility (start).

== v0.16.4

* Compatibility for admin statics in all Djangos

== v0.16.3

* Make it compatible with the latest FeinCMS (1.7.x) and Django (1.5).

== v0.16.2

* add makefile
* Renamed path variable
* Don't reset the self.page_path property

== v0.16.1

* Don't error out if there's not request in the context.

== v0.16

* Set related_name for videosection preview_mediafile.

== v0.15

* Fix `show_all_subnav` option of `feincms_page_menu` regression.
* Add Django 1.4 compatible MPTTFilterSpec.

== v1.14

* Get ancestor prepared_date based on url path.

== v0.13

* Add LICENSE
* Fix prepared_date admin extension. Add default=''.

== v0.12.1

* Tidy-up.
* Add ul_tag option to {% feincms_page_menu %} & refactor.

== v0.12.0

* Fix an import for FeinCMS 1.6.

== v0.11.6

* Add some region specific rendering options to MediaFileContent

== v0.11.5

* Heystack indexing template tweaks.

== v0.11.4

* It's late. I'm tired. Please work this time.

== v0.11.3

* Use correct path in template tag. I hope.

== v0.11.2

* Pass correct object into search index.

== v0.11.1


== v0.11.0

* Put files in correct location.
* Put files in correct location. Again.

== v0.11

* Oops typo!

== v0.10.1

* Add search indexing for haystack.
* Add txt files to manifest so we can use haystack.

== v0.10

* Tidied video content templates and added 'region' to render template search list.

== v0.9.4

* Added related_name to video fk

== v0.9.3

* Fixed feincms_page_menu extended navigation

== v0.9.2

* Fixed page navigation query when depth>1 and level=1

== v0.9.1

* Fix page_menu template tag to properly show all ancestors when on a page several levels deep. For a deep menu tree, the nav was not outputting the ancestors of the current page between the page level and the top level.

== v0.9

* Make maxcuna-navigation fall over quietly without navigation objects.
* Suppress `None` from being output when there are no Navigation items

== v0.8.1

* added `is_ancestor` flag to maxcuna-navigation

== v0.8

* removed daft import

== v0.7.2

* moving download related tags into django-incuna

== v0.7.1

* Return parent date if there isn't one on the current object
* Use the object instead of the class

== v0.7

* Add a get prepared date method

== v0.6.1

* Add prepared date page extension

== v0.6

* added accidentally omitted import

== v0.5

* added media-file related file-path filters originally from customer project

== v0.4.1

* Added MPTTModelChoiceField to admin form for page and parent navigation items to display hierarchy as indentaion. Updated help_text. Fixed unique dom_id clean.

== v0.4

* Added (mark) safe to menu item titles

== v0.3

* Added video content media

== v0.2

* Added video content
* Fixed version

== v0.1

* Check the admin class has show_on_top variable which isn't necessarily in FeinCMS
* Fixed manifest
* Automated merge with ssh://bitbucket.org/incuna/incuna-feincms
