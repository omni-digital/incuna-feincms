# incuna-feincms changelog

## CURRENT

* Update extensions to remove deprecated `register(cls, admin_cls)` format.
    * Update the prepared_date extension.
    * Update comments extension.
    * Update links extension.
    * Update mediafiles extension.
    * Update show_title extension.

## v1.1.0

* Use model._mptt_meta rather than model._meta.
  django-mptt  >= 0.4.0 moved the mptt options from model._mptt_meta
  to model._meta.
* Add changelog <=v0.15 based on git commit history.

## v1.0.3

* Fix typo in navigation admin form

## v1.0.2

* Add the current navigation level to the context.

## v1.0.1

* Add the current navigation level to the context.

## v1.0.0

*Note: Dropped support for FeinCMS < 1.7 and django 1.3.*

* Use `MediaFileForeignKey` for `VideoSectionContent`.

## v0.16.6

* Minor FeinCMS 1.7 fix.

## v0.16.5

* Fix for django >= 1.4 (try to use STATIC_URL over ADMIN_MEDIA_PREFIX).

## v0.16.4

* Remove `verify_exists` kwarg from `Navigation.url`.
* Fix some FeinCMS 1.7 imports. (FeinCMS had a refactor.)

## v0.16.3

* Fix cached template loader bug.
* Add Makefile.

## v0.16.2

* Don't fail hard in `{% incunafein_navigation %}` when request is not in context.

## v0.16.1

* Set related_name for videosection preview_mediafile.

## v0.16

* Add Django 1.4 compatible MPTTFilterSpec.
* Fix `show_all_subnav` option of `feincms_page_menu` regression.

## v0.15

* Fix `show_all_subnav` option of `feincms_page_menu` regression.
* Add Django 1.4 compatible MPTTFilterSpec.

## v1.14

* Get ancestor prepared_date based on url path.

## v0.13

* Add LICENSE
* Fix prepared_date admin extension. Add default=''.

## v0.12.1

* Tidy-up.
* Add ul_tag option to {% feincms_page_menu %} & refactor.

## v0.12.0

* Fix an import for FeinCMS 1.6.

## v0.11.6

* Add some region specific rendering options to MediaFileContent

## v0.11.5

* Heystack indexing template tweaks.

## v0.11.4

* It's late. I'm tired. Please work this time.

## v0.11.3

* Use correct path in template tag. I hope.

## v0.11.2

* Pass correct object into search index.

## v0.11.1


## v0.11.0

* Put files in correct location.
* Put files in correct location. Again.

## v0.11

* Oops typo!

## v0.10.1

* Add search indexing for haystack.
* Add txt files to manifest so we can use haystack.

## v0.10

* Tidied video content templates and added 'region' to render template search list.

## v0.9.4

* Added related_name to video fk

## v0.9.3

* Fixed feincms_page_menu extended navigation

## v0.9.2

* Fixed page navigation query when depth>1 and level=1

## v0.9.1

* Fix page_menu template tag to properly show all ancestors when on a page several levels deep. For a deep menu tree, the nav was not outputting the ancestors of the current page between the page level and the top level.

## v0.9

* Make maxcuna-navigation fall over quietly without navigation objects.
* Suppress `None` from being output when there are no Navigation items

## v0.8.2

* added `is_ancestor` flag to maxcuna-navigation

## v0.8

* removed daft import

## v0.7.2

* moving download related tags into django-incuna

## v0.7.1

* Return parent date if there isn't one on the current object
* Use the object instead of the class

## v0.7

* Add a get prepared date method

## v0.6.1

* Add prepared date page extension

## v0.6

* added accidentally omitted import

## v0.5

* added media-file related file-path filters originally from customer project

## v0.4.1

* Added MPTTModelChoiceField to admin form for page and parent navigation items to display hierarchy as indentaion. Updated help_text. Fixed unique dom_id clean.

## v0.4

* Added (mark) safe to menu item titles

## v0.3

* Added video content media

## v0.2

* Added video content
* Fixed version

## v0.1

* Check the admin class has show_on_top variable which isn't necessarily in FeinCMS
* Fixed manifest
* Automated merge with ssh://bitbucket.org/incuna/incuna-feincms
