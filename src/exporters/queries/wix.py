GET_FILTERED_PRODUCTS = """
query getFilteredProducts(
  $mainCollectionId: String!,
  $filters: ProductFilters,
  $sort: ProductSort,
  $offset: Int,
  $limit: Int,
  $withPriceRange: Boolean = false
) {
  catalog {
    category(categoryId: $mainCollectionId) {
      productsWithMetaData(
        filters: $filters,
        limit: $limit,
        sort: $sort,
        offset: $offset,
        onlyVisible: true
      ) {
        totalCount

        list {
          id
          name
         sku

          price
          formattedPrice

          comparePrice
          formattedComparePrice

          isInStock
          urlPart
          ribbon
          productType
          currency

          media {
            url
            fullUrl
            width
            height
            altText
          }

          inventory {
            status
            quantity
          }

          priceRange(withSubscriptionPriceRange: true)
            @include(if: $withPriceRange) {
            fromPrice
            fromPriceFormatted
          }
        }
      }
    }
  }
}
"""

GET_PRODUCT_BY_SLUG = """
query getProductBySlug(
  $externalId: String!,
  $slug: String!,
  $withPriceRange: Boolean = false
) {
  appSettings(externalId: $externalId) {
    widgetSettings
  }

  catalog {
    product(
      slug: $slug,
      onlyVisible: true
    ) {
      id
      description
      isVisible

      sku

      ribbon

      additionalRibbons {
        id
        name
      }

      brand

      price
      comparePrice
      discountedPrice

      formattedPrice
      formattedComparePrice
      formattedDiscountedPrice

      pricePerUnit
      formattedPricePerUnit

      pricePerUnitData {
        baseQuantity
        baseMeasurementUnit
      }

      breadcrumbs {
        id
        name
        slug
      }

      categories {
        id
        name
      }

      mainCategoryId
      categoryIds

      seoTitle
      seoDescription

      createVersion

      digitalProductFileItems {
        fileId
        fileType
        fileName
      }

      itemDiscount {
        discountRuleName
        automaticDiscountRuleNames
        priceAfterDiscount
        priceAfterDiscountAmount
        automaticDiscountPricePerUnit
        formattedAutomaticDiscountPricePerUnit
      }

      productItems(withDefaultVariant: true) {
        id

        price
        comparePrice

        formattedPrice
        formattedComparePrice

        hasDiscount

        automaticDiscount {
          automaticDiscountPrice
          formattedAutomaticDiscountPrice
          automaticDiscountPricePerUnit
          formattedAutomaticDiscountPricePerUnit
        }

        pricePerUnit
        formattedPricePerUnit

        optionsSelections

        isVisible
        availableForPreOrder
        isTrackingInventory

        inventory {
          status
          quantity
        }

        preOrderInfo {
          limit
          message
        }

        sku
        weight
        surcharge

        subscriptionPlans {
          list {
            id
            price
            formattedPrice
            pricePerUnit
            formattedPricePerUnit
          }
        }
      }

      name

      isTrackingInventory

      inventory {
        status
        quantity
        availableForPreOrder

        preOrderInfoView {
          message
          preOrder
          limit
        }
      }

      isManageProductItems
      productItemsPreOrderAvailability

      isInStock

      media {
        id
        url
        fullUrl

        altText

        thumbnailFullUrl: fullUrl(
          width: 50
          height: 50
        )

        mediaType
        videoType

        videoFiles {
          url
          width
          height
          format
          quality
        }

        width
        height
        index
        title
      }

      customTextFields {
        key
        title
        isMandatory
        inputLimit
      }

      nextOptionsSelectionId

      options {
        id
        title
        optionType
        key

        selections {
          id
          value
          description
          key

          linkedMediaItems {
            altText
            url
            fullUrl

            thumbnailFullUrl: fullUrl(
              width: 50
              height: 50
            )

            mediaType

            width
            height
            index
            title

            videoFiles {
              url
              width
              height
              format
              quality
            }
          }

          displayImage {
            id
            url
            height
            width
            altText
          }
        }
      }

      productType

      urlPart

      additionalInfo {
        id
        title
        description
        index
      }

      subscriptionPlans {
        list(onlyVisible: true) {
          id
          name
          tagline
          frequency
          interval
          duration

          price
          formattedPrice

          pricePerUnit
          formattedPricePerUnit
        }

        oneTimePurchase {
          index
        }
      }

      priceRange(withSubscriptionPriceRange: true)
        @include(if: $withPriceRange) {
        fromPrice
        fromPriceFormatted
      }

      discount {
        mode
        value
      }

      currency

      weight

      seoJson

      groupInfo {
        productGroupId
        groupingCustomizationId

        members {
          productId

          choice {
            id
            value
            description
            key
          }

          slug
          inventoryAvailabilityStatus
        }
      }
    }
  }
}
"""