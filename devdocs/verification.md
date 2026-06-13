> ## Documentation Index
> Fetch the complete documentation index at: https://docs.vouched.id/llms.txt
> Use this file to discover all available pages before exploring further.

# API Overview

The Vouched API allows you to [submit](https://docs.vouched.id/reference/submitjob), [find](https://docs.vouched.id/reference/findjobs-1), or [download](https://docs.vouched.id/reference/downloadjobpdf-1) identity verification jobs. You can also submit [driver license verification jobs](https://docs.vouched.id/reference/submitdlv-1), [crosscheck jobs](https://docs.vouched.id/reference/crosscheck-3), and [invite users](https://docs.vouched.id/reference/sendinvites-1) to verify through a Vouched hosted flow.

> 📘 Create an Account
>
> Before proceeding, [create an account](https://www.vouched.id/get-started/) so you can obtain a key and use our API.

## Authentication

Vouched authenticates your requests using your keys. If the key is missing or incorrect in your request, Vouched will not process the request and return an unauthenticated error. API access and data is encrypted in transit using TLS 1.2.

To create your private key for this API, see the [Manage Keys](https://docs.vouched.id/docs/manage-keys) section.

| Security Scheme Type | Header Parameter Name |
| :------------------- | :-------------------- |
| API Key              | `X-API-Key`           |

## Testing the API

You can test our API directly from this documentation site. Simply paste your private key into the **Authentication** box on any endpoint page, then click **Try It** to test the call and see the response.

<Image title="api-docs.png" alt={1131} border={true} src="https://files.readme.io/b350507-api-docs.png">
  Testing API Calls
</Image>

> 🚧 Payload Limits
>
> Please note: the [Submit Job](https://docs.vouched.id/reference/submitjob) endpoint has a payload limit of 20MB. If a request over 20MB is made, we'll return a 413 error.

## Example Code

Example use cases for our API are available in [Python](https://github.com/vouched/vouched-python-example) , [Java](https://github.com/vouched/vouched-java-example), [React](https://github.com/vouched/vouched-react-example) and [NodeJS](https://github.com/vouched/vouched-nodejs-example).

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.vouched.id/llms.txt
> Use this file to discover all available pages before exploring further.

# Postman API Package

![300](https://files.readme.io/abe72ae-postman.png "postman.png")

Our Postman collection package can help you test our API and integrate it with your code. The package contains all our APIs and can be loaded to your Postman client app at the click of a button.

Before sending a call:

* In the **Headers** tab switch `{{Private_Key}}` to your `private key` from the Vouched dashboard (x-api-key).
* Comments // are not supported via JSON API calls, when applicable please remove all the comments. We placed them as an initial explanation of certain fields.
* When applicable change URL query params to your relevant configurations.
* Fields that are marked as **optional** can be deleted if not required for your personal use case.

![1039](https://files.readme.io/02dbce6-123.png "123.png")

<br />

<br />

<br />

## Download and import the package

<br />

Download the file:

<Embed url="https://drive.google.com/file/d/1S742INtnzBCJiKq4fIxXrwo8OfytGBbT/view?usp=sharing" title="Vouched API Package.postman_collection.json" favicon="https://ssl.gstatic.com/images/branding/product/1x/drive_2020q4_32dp.png" provider="drive.google.com" href="https://drive.google.com/file/d/1S742INtnzBCJiKq4fIxXrwo8OfytGBbT/view?usp=sharing" />

In the **Collection** menu click **Import** and add the file:

![435](https://files.readme.io/350ab4b-1234.png "1234.png")

Done! Your new Vouched API Package is ready to use.





> ## Documentation Index
> Fetch the complete documentation index at: https://docs.vouched.id/llms.txt
> Use this file to discover all available pages before exploring further.

# Submit Identity CrossCheck

Provides a crosscheck of matching identities based on provided name, email, phone number, address, and IP address. The crosscheck is performed across a network of enriched data sources.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "version": "0.13.13",
    "title": "Vouched API",
    "description": "Official Vouched REST API",
    "x-logo": {
      "url": "https://i.pinimg.com/originals/88/29/2f/88292f8ffd6231d0c41634f2e707c34a.png",
      "altText": "Vouched logo"
    },
    "license": {
      "name": "Apache 2.0",
      "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
  },
  "servers": [
    {
      "url": "https://verify.vouched.id"
    }
  ],
  "tags": [
    {
      "name": "crosscheck",
      "description": "This is the section where you will do actions for all things related to CrossCheck."
    }
  ],
  "paths": {
    "/api/identity/crosscheck": {
      "post": {
        "description": "Provides a crosscheck of matching identities based on provided name, email, phone number, address, and IP address. The crosscheck is performed across a network of enriched data sources.",
        "summary": "Submit Identity CrossCheck",
        "operationId": "crossCheck",
        "security": [
          {
            "X-API-Key": []
          }
        ],
        "tags": [
          "crosscheck"
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/crosscheck_request"
              },
              "examples": {
                "0": {
                  "value": {
                    "firstName": "John",
                    "lastName": "Bao",
                    "email": "test@test.acme.com",
                    "phone": "000-111-2222",
                    "ipAddress": "73.19.102.110",
                    "address": {
                      "unit": "",
                      "streetAddress": "123 Elmo Avenue",
                      "city": "Seattle",
                      "state": "WA",
                      "postalCode": "98109",
                      "country": "US"
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Crosschecking a job",
            "content": {
              "application/json; charset=utf-8": {
                "schema": {
                  "$ref": "#/components/schemas/identity_crosscheck"
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/400"
          },
          "401": {
            "$ref": "#/components/responses/401"
          },
          "404": {
            "$ref": "#/components/responses/404"
          },
          "429": {
            "$ref": "#/components/responses/429"
          },
          "500": {
            "$ref": "#/components/responses/500"
          }
        },
        "servers": [
          {
            "url": "https://verify.vouched.id"
          }
        ]
      },
      "servers": [
        {
          "url": "https://verify.vouched.id"
        }
      ]
    }
  },
  "components": {
    "securitySchemes": {
      "X-API-Key": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
        "description": "The authentication private key"
      }
    },
    "schemas": {
      "gender_distribution": {
        "type": "object",
        "properties": {
          "man": {
            "type": "integer",
            "description": "frequency with a range 0-100 of the first name in men with a mininum found frequency of 0.0001",
            "minimum": 0,
            "maximum": 100
          },
          "woman": {
            "type": "integer",
            "description": "frequency with a range 0-100 of the first name in women with a mininum found frequency of 0.0001",
            "minimum": 0,
            "maximum": 100
          }
        }
      },
      "crosscheck_identity_errors": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "description": "Type of error encountered."
          },
          "warnings": {
            "type": "boolean",
            "description": "Is this a warning?"
          },
          "message": {
            "type": "string",
            "description": "Details on the occurring error."
          },
          "suggestion": {
            "type": "string",
            "example": "John Smith",
            "description": "A suggestion for matching name."
          }
        }
      },
      "crosscheck_age_range": {
        "type": "object",
        "properties": {
          "from": {
            "type": "integer",
            "description": "From age"
          },
          "to": {
            "type": "integer",
            "description": "To age"
          }
        }
      },
      "crosscheck_identity_address": {
        "type": "object",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "warnings": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "isValid": {
            "type": "boolean",
            "description": "The address is a verified address."
          },
          "isMatch": {
            "type": "boolean",
            "description": "The name on the address matches the user."
          },
          "name": {
            "type": "string",
            "description": "The recorded name of the identity."
          },
          "ageRange": {
            "description": "The age range of the name on the address.",
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "isForwarder": {
            "type": "boolean",
            "description": "The address is a freight forwarding address."
          },
          "isCommercial": {
            "type": "boolean",
            "description": "The address is associated with a business."
          },
          "type": {
            "type": "string",
            "enum": [
              "incomplete-address",
              "po-box",
              "multi-unit",
              "single-unit",
              "commercial-mail-drop",
              "po-box-forward",
              "other"
            ]
          }
        }
      },
      "crosscheck_identity_email": {
        "type": "object",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "warnings": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "isValid": {
            "type": "boolean",
            "description": "The email is a valid email address."
          },
          "isMatch": {
            "type": "boolean",
            "description": "The name associated with the email address matches the user."
          },
          "name": {
            "type": "string",
            "description": "The recorded name of the identity."
          },
          "ageRange": {
            "description": "The age range of the name on the email address.",
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "isAutoGenerated": {
            "type": "boolean",
            "description": "Indicates the email address was generated automatically."
          },
          "isDisposable": {
            "type": "boolean",
            "description": "The email address is provided by a disposable email provider."
          },
          "daysFirstSeen": {
            "type": "integer",
            "description": "The number of days since the email address was first seen in the data network."
          }
        }
      },
      "crosscheck_identity_phone": {
        "type": "object",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "warnings": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "isValid": {
            "type": "boolean",
            "description": "The phone number is valid."
          },
          "isMatch": {
            "type": "boolean",
            "description": "The name associated with the phone number matches the user."
          },
          "name": {
            "type": "string",
            "description": "The recorded name of the identity."
          },
          "type": {
            "type": "string",
            "enum": [
              "fixed-voip",
              "landline",
              "mobile",
              "non-fixed-voip",
              "premium-rate",
              "tollfree",
              "voicemail",
              "other"
            ]
          },
          "ageRange": {
            "description": "The age range of the name associated with the phone number.",
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "carrier": {
            "type": "string",
            "description": "The phone provider."
          },
          "isPrepaid": {
            "type": "boolean",
            "description": "The phone number is on a prepaid plan."
          },
          "isDisposable": {
            "type": "boolean",
            "description": "The phone number is disposable."
          },
          "isCommercial": {
            "type": "boolean",
            "description": "The phone number is associated with a business."
          }
        }
      },
      "location": {
        "type": "object",
        "properties": {
          "latitude": {
            "type": "number"
          },
          "longitude": {
            "type": "number"
          }
        }
      },
      "ip_address": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "Originating City."
          },
          "state": {
            "type": "string",
            "description": "Originating State/Province/Territory in [ISO 3166-2 code](https://en.wikipedia.org/wiki/ISO_3166-2)."
          },
          "country": {
            "type": "string",
            "description": "Originating Country in [ISO 3166-1 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)."
          },
          "postalCode": {
            "type": "string",
            "description": "postal code."
          },
          "location": {
            "type": "object",
            "$ref": "#/components/schemas/location"
          },
          "isp": {
            "type": "string",
            "description": "Name of the isp."
          },
          "organization": {
            "type": "string",
            "description": "Name of the organization associated with the IP address."
          },
          "isAnonymous": {
            "type": "boolean",
            "description": "Is the IP address part of an anonymous network."
          },
          "isAnonymousVpn": {
            "type": "boolean",
            "description": "Is the IP address part of an anonymous vpn network."
          },
          "isAnonymousHosting": {
            "type": "boolean",
            "description": "Is the IP address part of an anonymous hosting network."
          },
          "userType": {
            "type": "string",
            "description": "A description of the internet access point.",
            "enum": [
              "business - the IP address belongs to a business ISP or a corporation.",
              "cafe - an internet cafe or similar location.",
              "cellular - the IP address is used to route traffic from devices connected to a cellular network.",
              "college - the IP address belongs to a college, university, or similar institute of higher education.",
              "content_delivery_network - belongs to a CDN (Akamai, Cloudflare, Google Cloud, etc.).",
              "dialup - belongs to a dial-up ISP.",
              "government - the IP address belongs to a government organization.",
              "hosting -- a commercial hosting provider.",
              "library - used in a library.",
              "military - used on a military base or similar.",
              "residential - the IP address belongs to a residential ISP or is otherwise primarily used by home users.",
              "router - a backbone or infrastructure router.",
              "school - primary or secondary education.",
              "search_engine_spider - a crawler or indexer for a search engine (Google, Bing, Yahoo, etc.).",
              "traveler - the IP address is used at an airport, hotel, or similar location where the users are generally traveling from their primary residence."
            ]
          }
        }
      },
      "crosscheck_darkweb": {
        "type": "object",
        "properties": {
          "criminalCount": {
            "type": "integer",
            "description": "Count of instances email was observed to have been used in DarkWeb data collections."
          },
          "criminalLastSeen": {
            "type": "string",
            "description": "Last observed time email was observed to have been used in DarkWeb collections."
          },
          "criminalMaxScore": {
            "type": "integer",
            "description": "0-low risk, 5-critical risk.",
            "minimum": 0,
            "maximum": 5
          }
        }
      },
      "crosscheck_confidences": {
        "type": "object",
        "properties": {
          "identity": {
            "type": "number",
            "description": "Overall identity risk confidence. The identity score is a risk score assigned to the user based on their address, email, and phone details. These details are cross-referenced against the data provided by the user or the extracted from their ID.",
            "minimum": 0,
            "maximum": 1
          },
          "activity": {
            "type": [
              "number",
              "null"
            ],
            "description": "Overall activity risk confidence that is based on dynamic attributes."
          }
        }
      },
      "crosscheck_result": {
        "type": "object",
        "description": "CrossCheck Result",
        "properties": {
          "address": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_identity_address"
          },
          "email": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_identity_email"
          },
          "phone": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_identity_phone"
          },
          "gender": {
            "type": "object",
            "$ref": "#/components/schemas/gender_distribution"
          },
          "ageRange": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "ipAddress": {
            "type": "object",
            "$ref": "#/components/schemas/ip_address"
          },
          "darkWeb": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_darkweb"
          },
          "confidences": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_confidences"
          }
        }
      },
      "error": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "description": "\nError type code.\n- InvalidRequestError - The request is invalid.\n\n  - Parameters sent in the request are invalid.\n\n\n- FaceMatchError - The face match score was lower than the threshold.\n\n  - Category: faceMatch\n\n  - Faces obtained from the ID and Selfie images do not match.\n\n\n- NameMatchError - The name match score was lower than the threshold.\n\n  - The name provided by the user and the name extracted from the ID do not match.\n\n  - Eg: User Provided Name - Dave Smith, Extracted Name - David Smith\n\n\n- BarcodeMatchError - The barcode match score was lower than the threshold.\n\n  - The data provided by the user and the data extracted from the barcode do not match. \n\n  - Eg: User Provided Name - Dave Smith, Extracted Name - David Smith\n\n\n- BirthDateMatchError - The birth date match score was lower than the threshold.\n\n  - The birth date provided by the user and the data extracted from the ID do not match.\n\n  - Eg: User Provided DOB - 01/09/1992, Extracted DOB - 09/01/1992\n\n  - Eg: User Provided DOB - 11/09/1992, Extracted DOB - 12/09/1992\n\n\n- ExpiredIdError - The ID’s expiration date has passed.\n\n  - The expiration date extracted from the ID indicates that it has expired.\n\n- InvalidIdPhotoError - The ID is invalid.\n\n  - Category: id\n\n  - The image submitted does not qualify as an ID. The ID image may be of lower quality, have blur, glare or it may be too dark, and hence the data could not be extracted.\n\n- InvalidUserPhotoError - The user photo (selfie) is invalid.\n\n  - Category: selfie\n\n  - The image submitted does not qualify as a selfie.\n\n- AuthenticationError - The request could not be authenticated.\n\n  - The key could not be verified.\n\n- ConnectionError - A connection error occurred while communicating to the Vouched service.\n\n  - UnknownSystemError - A unknown system error occurred.\n\n- TooManyRequestsError - the Vouched service has throttled this request.\n\n  - Retry your request later.\n\n- UnprocessableContentError - The request contains incorrectly formatted or missing data.\n\n  - The server understood the content type of the request content, and the syntax of the request content was correct, but it was unable to process the contained instructions.\n\n  - Eg: Submitted data contains invalid characters\n\n  - Eg: Required data is missing",
            "enum": [
              "InvalidRequestError",
              "FaceMatchError",
              "NameMatchError",
              "BarcodeMatchError",
              "BirthDateMatchError",
              "ExpiredIdError",
              "InvalidIdPhotoError",
              "InvalidUserPhotoError",
              "AuthenticationError",
              "ConnectionError",
              "UnknownSystemError",
              "TooManyRequestsError",
              "UnprocessableContentError"
            ]
          },
          "message": {
            "type": "string",
            "description": "Details on the occurring error."
          },
          "warning": {
            "type": "boolean",
            "description": "Is this a warning?"
          },
          "suggestion": {
            "example": "John Smith",
            "description": "A suggestion for matching name.",
            "type": "string"
          }
        }
      },
      "errors": {
        "type": "object",
        "description": "List of errors for unsuccessful completed jobs.",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/error"
            }
          }
        }
      },
      "base_address": {
        "type": "object",
        "description": "Address",
        "properties": {
          "unit": {
            "type": "string",
            "description": "Unit number."
          },
          "streetAddress": {
            "type": "string",
            "description": "Street Address."
          },
          "city": {
            "type": "string",
            "description": "City."
          },
          "state": {
            "type": "string",
            "description": "Two-character state code associated with the phone number. [state code](https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html)"
          },
          "postalCode": {
            "type": "string",
            "description": "Postal Code."
          },
          "country": {
            "type": "string",
            "description": "The [ISO 3166-1 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)."
          }
        }
      },
      "crosscheck_request": {
        "type": "object",
        "description": "CrossCheck Request",
        "properties": {
          "email": {
            "type": "string",
            "description": "Email address."
          },
          "phone": {
            "type": "string",
            "description": "Phone number. Defaults to +1 (US and CA). Country code required for other countries.",
            "example": "000-111-2222"
          },
          "firstName": {
            "type": "string",
            "description": "First Name."
          },
          "lastName": {
            "type": "string",
            "description": "Last Name."
          },
          "address": {
            "type": "object",
            "$ref": "#/components/schemas/base_address"
          },
          "ipAddress": {
            "type": "string",
            "description": "IP Address."
          }
        },
        "required": [
          "firstName",
          "lastName"
        ]
      },
      "identity_crosscheck": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "ID of the request."
          },
          "request": {
            "type": "object",
            "description": "Request object for crosscheck.",
            "$ref": "#/components/schemas/crosscheck_request"
          },
          "result": {
            "type": "object",
            "description": "Result object for crosscheck.",
            "$ref": "#/components/schemas/crosscheck_result"
          }
        }
      }
    },
    "responses": {
      "400": {
        "description": "InvalidRequestError - The request is invalid.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "InvalidRequestError",
                  "message": "Invalid request"
                }
              ]
            }
          }
        }
      },
      "401": {
        "description": "AuthenticationError - The request could not be authenticated.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "AuthenticationError",
                  "message": "Unauthorized access"
                }
              ]
            }
          }
        }
      },
      "404": {
        "description": "ConnectionError - A connection error occurred while communicating to the Vouched service.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "ConnectionError",
                  "message": "Connection error"
                }
              ]
            }
          }
        }
      },
      "429": {
        "description": "TooManyRequestsError - the Vouched service has throttled this request.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "TooManyRequestsError",
                  "message": "Too many requests error"
                }
              ]
            }
          }
        }
      },
      "500": {
        "description": "UnknownSystemError - A unknown system error occurred.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "UnknownSystemError",
                  "message": "Oops, we encountered a problem"
                }
              ]
            }
          }
        }
      }
    }
  },
  "x-tagGroups": [
    {
      "name": "APIs",
      "tags": [
        "jobs",
        "invites",
        "crosscheck",
        "aml",
        "ssn",
        "tin",
        "dob",
        "documents"
      ]
    }
  ]
}
```



> ## Documentation Index
> Fetch the complete documentation index at: https://docs.vouched.id/llms.txt
> Use this file to discover all available pages before exploring further.

# Find Jobs

Return paginated jobs

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "version": "0.13.13",
    "title": "Vouched API",
    "description": "Official Vouched REST API",
    "x-logo": {
      "url": "https://i.pinimg.com/originals/88/29/2f/88292f8ffd6231d0c41634f2e707c34a.png",
      "altText": "Vouched logo"
    },
    "license": {
      "name": "Apache 2.0",
      "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
  },
  "servers": [
    {
      "url": "https://verify.vouched.id"
    }
  ],
  "tags": [
    {
      "name": "jobs",
      "description": "This is the section where you will do actions for all things related to running, completing, and getting the results of Jobs."
    }
  ],
  "paths": {
    "/api/jobs": {
      "get": {
        "description": "Return paginated jobs",
        "summary": "Find Jobs",
        "operationId": "findJobs",
        "security": [
          {
            "X-API-Key": []
          }
        ],
        "tags": [
          "jobs"
        ],
        "parameters": [
          {
            "name": "id",
            "in": "query",
            "description": "Filter by job ID.",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "internalId",
            "in": "query",
            "description": "Filter by internal ID set by your organization when the job was created.",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "type",
            "in": "query",
            "description": "Filter by job type.",
            "schema": {
              "type": "string",
              "enum": [
                "id-verification"
              ]
            }
          },
          {
            "name": "fields",
            "in": "query",
            "description": "Filter the fields returned. Separate multiple fields with commas. For nested fields, use dot notation.",
            "example": "result.firstName,result.lastName,completed",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "ids",
            "in": "query",
            "description": "Filter by a list of job IDs.",
            "example": [
              "AteDNdD",
              "jiorhBJDs"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          {
            "name": "token",
            "in": "query",
            "description": "The time limited session token from the web client.",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "page",
            "in": "query",
            "description": "Paginate list by page.",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "default": 1
            }
          },
          {
            "name": "pageSize",
            "in": "query",
            "description": "The number of items for a page.",
            "schema": {
              "type": "integer",
              "default": 100,
              "maximum": 250
            }
          },
          {
            "name": "sortBy",
            "in": "query",
            "description": "Selection to sort list from.",
            "schema": {
              "type": "string",
              "enum": [
                "submitted",
                "updated",
                "status"
              ]
            }
          },
          {
            "name": "sortOrder",
            "in": "query",
            "description": "Order the sort.",
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ]
            }
          },
          {
            "name": "status",
            "in": "query",
            "description": "Filter by status.",
            "schema": {
              "type": "string",
              "enum": [
                "active",
                "completed",
                "removed"
              ]
            }
          },
          {
            "name": "aml",
            "in": "query",
            "description": "Filter by AML match type.",
            "schema": {
              "type": "string",
              "enum": [
                "sanction",
                "warning",
                "pep",
                "all"
              ]
            }
          },
          {
            "name": "from",
            "in": "query",
            "description": "Filter by submitted/updatedAt from the [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601).",
            "example": "2019-09-07T15:50-04:00",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "to",
            "in": "query",
            "description": "Filter by submitted/updatedAt to the [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601).",
            "example": "2019-09-07T15:50-04:00",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "toFrom",
            "in": "query",
            "description": "Filter to and from.",
            "schema": {
              "type": "string",
              "default": "submitted",
              "enum": [
                "submitted",
                "updatedAt"
              ]
            }
          },
          {
            "name": "withPhotos",
            "in": "query",
            "description": "Job will contain idPhoto and userPhoto photos. Maximum 100 returned.",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          },
          {
            "name": "withPhotoUrls",
            "in": "query",
            "description": "Job will contain idPhotoUrl and userPhotoUrl signed. Maximum 100 returned.",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Provide Results on Jobs.",
            "content": {
              "application/json; charset=utf-8": {
                "schema": {
                  "$ref": "#/components/schemas/result_jobs"
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/400"
          },
          "401": {
            "$ref": "#/components/responses/401"
          },
          "404": {
            "$ref": "#/components/responses/404"
          },
          "429": {
            "$ref": "#/components/responses/429"
          },
          "500": {
            "$ref": "#/components/responses/500"
          }
        }
      },
      "servers": [
        {
          "url": "https://verify.vouched.id"
        }
      ]
    }
  },
  "components": {
    "securitySchemes": {
      "X-API-Key": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
        "description": "The authentication private key"
      }
    },
    "schemas": {
      "request_info": {
        "type": "object",
        "properties": {
          "ipaddress": {
            "description": "The user's IP address.",
            "type": "string"
          },
          "useragent": {
            "description": "The user's browser agent.",
            "type": "string"
          },
          "referer": {
            "description": "The refering browser location.",
            "type": "string"
          }
        }
      },
      "job_parameters": {
        "type": "object",
        "properties": {
          "idPhoto": {
            "description": "The user's official identification photo in base64.",
            "type": "string"
          },
          "idPhotoUrl": {
            "description": "The user's id photo as a timed (15 min) signed url.",
            "type": "string"
          },
          "idPhotoDetect": {
            "description": "A cropped aligned version of the id photo in base64.",
            "type": "string"
          },
          "idPhotoDetectUrl": {
            "description": "A cropped aligned version of the id photo as timed (15 min) signed url.",
            "type": "string"
          },
          "idPhotoDetectDimensions": {
            "type": "object",
            "properties": {
              "width": {
                "description": "width of photo",
                "type": "integer"
              },
              "height": {
                "description": "height of photo",
                "type": "integer"
              }
            }
          },
          "idPhotoDimensions": {
            "type": "object",
            "properties": {
              "width": {
                "description": "width of photo",
                "type": "integer"
              },
              "height": {
                "description": "height of photo",
                "type": "integer"
              }
            }
          },
          "backIdPhoto": {
            "description": "The back of the user's official identification photo in base64.",
            "type": "string"
          },
          "backIdPhotoUrl": {
            "description": "The back of the user's id photo as a timed (15 min) signed url.",
            "type": "string"
          },
          "backIdPhotoDimensions": {
            "type": "object",
            "properties": {
              "width": {
                "description": "width of photo",
                "type": "integer"
              },
              "height": {
                "description": "height of photo",
                "type": "integer"
              }
            }
          },
          "userPhoto": {
            "description": "The user's selfie photo in base64.",
            "type": "string"
          },
          "userPhotoUrl": {
            "description": "The user's selfie photo as a timed (15 min) signed url.",
            "type": "string"
          },
          "userPhotoDetect": {
            "description": "A cropped aligned version of the selfie photo in base64.",
            "type": "string"
          },
          "userPhotoDetectUrl": {
            "description": "A cropped aligned version of the selfie photo as timed (15 min) signed url.",
            "type": "string"
          },
          "userPhotoDetectDimensions": {
            "type": "object",
            "properties": {
              "width": {
                "description": "width of photo",
                "type": "integer"
              },
              "height": {
                "description": "height of photo",
                "type": "integer"
              }
            }
          },
          "userPhotoDimensions": {
            "type": "object",
            "properties": {
              "width": {
                "description": "width of photo",
                "type": "integer"
              },
              "height": {
                "description": "height of photo",
                "type": "integer"
              }
            }
          },
          "email": {
            "type": "string",
            "description": "Used for crosschecking identity."
          },
          "phone": {
            "type": "string",
            "description": "Used for crosschecking identity.",
            "example": "000-111-2222"
          },
          "dob": {
            "type": "string",
            "description": "Date of birth (MM/DD/YYYY).",
            "pattern": "^\\d{2}\\/\\d{2}\\/\\d{4}$",
            "example": "08/23/1991"
          },
          "firstName": {
            "type": "string",
            "description": "The user's first name."
          },
          "lastName": {
            "type": "string",
            "description": "The user's last name."
          }
        }
      },
      "request": {
        "type": "object",
        "properties": {
          "type": {
            "description": "Job type",
            "type": "string",
            "enum": [
              "drivers-license",
              "identification",
              "passport",
              "handgun",
              "residence",
              "global-entry",
              "employment",
              "drivers-license-permit",
              "nexus",
              "indian",
              "health-insurance",
              "commercial-license"
            ]
          },
          "callbackURL": {
            "description": "Upon the job's completion, Vouched will POST the job results to the defined [webhook](https://docs.vouched.id/docs/webhooks).",
            "type": "string"
          },
          "requestInfo": {
            "description": "User request information.",
            "type": "object",
            "$ref": "#/components/schemas/request_info"
          },
          "parameters": {
            "description": "Object for 'id-verification.'",
            "type": "object",
            "$ref": "#/components/schemas/job_parameters"
          }
        }
      },
      "gender_distribution": {
        "type": "object",
        "properties": {
          "man": {
            "type": "integer",
            "description": "frequency with a range 0-100 of the first name in men with a mininum found frequency of 0.0001",
            "minimum": 0,
            "maximum": 100
          },
          "woman": {
            "type": "integer",
            "description": "frequency with a range 0-100 of the first name in women with a mininum found frequency of 0.0001",
            "minimum": 0,
            "maximum": 100
          }
        }
      },
      "gender_info": {
        "type": "object",
        "properties": {
          "gender": {
            "description": "man or woman based on extracted fields from the ID.",
            "type": "string",
            "enum": [
              "man",
              "woman"
            ]
          },
          "genderDistribution": {
            "description": "frequency with a range 0-100 of the first name in men and women with a mininum found frequency of 0.0001",
            "type": "string",
            "$ref": "#/components/schemas/gender_distribution"
          }
        }
      },
      "client_data": {
        "type": "object",
        "properties": {
          "client": {
            "type": "string",
            "description": "Client on which the job was initialized."
          },
          "theme": {
            "type": "string"
          },
          "capture": {
            "type": "object",
            "description": "Type of image capture for each stage in the IDV process.",
            "properties": {
              "id": {
                "type": "string",
                "enum": [
                  "manual",
                  "automatic"
                ]
              },
              "face_match": {
                "type": "string",
                "enum": [
                  "manual",
                  "automatic"
                ]
              },
              "barcode": {
                "type": "string",
                "enum": [
                  "manual",
                  "automatic"
                ]
              }
            }
          }
        }
      },
      "ipFraudCheck": {
        "type": "object",
        "description": "Indicator of IP address fraud. The max attempts (default - 4) before a fraud check is triggered and the time range (default - 60 minutes) for the inspection is configurable.",
        "properties": {
          "ipFraud": {
            "type": "boolean",
            "description": "A boolean determining whether or not the ipAddress for the job was flagged as fraudulent."
          },
          "count": {
            "type": "integer",
            "description": "Represents the number of jobs with the same IP address."
          },
          "jobIdList": {
            "type": "array",
            "description": "List of job ids with the same IP address. Provides a maximum of 10 job IDs linked to the IP address.",
            "items": {
              "type": "string"
            }
          }
        }
      },
      "address": {
        "type": "object",
        "properties": {
          "unit": {
            "type": "string",
            "description": "Unit number."
          },
          "streetNumber": {
            "type": "string"
          },
          "street": {
            "type": "string"
          },
          "city": {
            "type": "string"
          },
          "state": {
            "type": "string",
            "description": "The [ISO 3166-2 state/province/territory code](https://en.wikipedia.org/wiki/ISO_3166-2)."
          },
          "postalCode": {
            "type": "string"
          },
          "postalCodeSuffix": {
            "type": "string"
          },
          "country": {
            "type": "string",
            "description": "The [ISO 3166-1 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)."
          }
        }
      },
      "crosscheck_identity_errors": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "description": "Type of error encountered."
          },
          "warnings": {
            "type": "boolean",
            "description": "Is this a warning?"
          },
          "message": {
            "type": "string",
            "description": "Details on the occurring error."
          },
          "suggestion": {
            "type": "string",
            "example": "John Smith",
            "description": "A suggestion for matching name."
          }
        }
      },
      "crosscheck_age_range": {
        "type": "object",
        "properties": {
          "from": {
            "type": "integer",
            "description": "From age"
          },
          "to": {
            "type": "integer",
            "description": "To age"
          }
        }
      },
      "crosscheck_identity_address": {
        "type": "object",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "warnings": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "isValid": {
            "type": "boolean",
            "description": "The address is a verified address."
          },
          "isMatch": {
            "type": "boolean",
            "description": "The name on the address matches the user."
          },
          "name": {
            "type": "string",
            "description": "The recorded name of the identity."
          },
          "ageRange": {
            "description": "The age range of the name on the address.",
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "isForwarder": {
            "type": "boolean",
            "description": "The address is a freight forwarding address."
          },
          "isCommercial": {
            "type": "boolean",
            "description": "The address is associated with a business."
          },
          "type": {
            "type": "string",
            "enum": [
              "incomplete-address",
              "po-box",
              "multi-unit",
              "single-unit",
              "commercial-mail-drop",
              "po-box-forward",
              "other"
            ]
          }
        }
      },
      "crosscheck_identity_email": {
        "type": "object",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "warnings": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "isValid": {
            "type": "boolean",
            "description": "The email is a valid email address."
          },
          "isMatch": {
            "type": "boolean",
            "description": "The name associated with the email address matches the user."
          },
          "name": {
            "type": "string",
            "description": "The recorded name of the identity."
          },
          "ageRange": {
            "description": "The age range of the name on the email address.",
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "isAutoGenerated": {
            "type": "boolean",
            "description": "Indicates the email address was generated automatically."
          },
          "isDisposable": {
            "type": "boolean",
            "description": "The email address is provided by a disposable email provider."
          },
          "daysFirstSeen": {
            "type": "integer",
            "description": "The number of days since the email address was first seen in the data network."
          }
        }
      },
      "crosscheck_identity_phone": {
        "type": "object",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "warnings": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/crosscheck_identity_errors"
            }
          },
          "isValid": {
            "type": "boolean",
            "description": "The phone number is valid."
          },
          "isMatch": {
            "type": "boolean",
            "description": "The name associated with the phone number matches the user."
          },
          "name": {
            "type": "string",
            "description": "The recorded name of the identity."
          },
          "type": {
            "type": "string",
            "enum": [
              "fixed-voip",
              "landline",
              "mobile",
              "non-fixed-voip",
              "premium-rate",
              "tollfree",
              "voicemail",
              "other"
            ]
          },
          "ageRange": {
            "description": "The age range of the name associated with the phone number.",
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "carrier": {
            "type": "string",
            "description": "The phone provider."
          },
          "isPrepaid": {
            "type": "boolean",
            "description": "The phone number is on a prepaid plan."
          },
          "isDisposable": {
            "type": "boolean",
            "description": "The phone number is disposable."
          },
          "isCommercial": {
            "type": "boolean",
            "description": "The phone number is associated with a business."
          }
        }
      },
      "location": {
        "type": "object",
        "properties": {
          "latitude": {
            "type": "number"
          },
          "longitude": {
            "type": "number"
          }
        }
      },
      "ip_address": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "Originating City."
          },
          "state": {
            "type": "string",
            "description": "Originating State/Province/Territory in [ISO 3166-2 code](https://en.wikipedia.org/wiki/ISO_3166-2)."
          },
          "country": {
            "type": "string",
            "description": "Originating Country in [ISO 3166-1 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)."
          },
          "postalCode": {
            "type": "string",
            "description": "postal code."
          },
          "location": {
            "type": "object",
            "$ref": "#/components/schemas/location"
          },
          "isp": {
            "type": "string",
            "description": "Name of the isp."
          },
          "organization": {
            "type": "string",
            "description": "Name of the organization associated with the IP address."
          },
          "isAnonymous": {
            "type": "boolean",
            "description": "Is the IP address part of an anonymous network."
          },
          "isAnonymousVpn": {
            "type": "boolean",
            "description": "Is the IP address part of an anonymous vpn network."
          },
          "isAnonymousHosting": {
            "type": "boolean",
            "description": "Is the IP address part of an anonymous hosting network."
          },
          "userType": {
            "type": "string",
            "description": "A description of the internet access point.",
            "enum": [
              "business - the IP address belongs to a business ISP or a corporation.",
              "cafe - an internet cafe or similar location.",
              "cellular - the IP address is used to route traffic from devices connected to a cellular network.",
              "college - the IP address belongs to a college, university, or similar institute of higher education.",
              "content_delivery_network - belongs to a CDN (Akamai, Cloudflare, Google Cloud, etc.).",
              "dialup - belongs to a dial-up ISP.",
              "government - the IP address belongs to a government organization.",
              "hosting -- a commercial hosting provider.",
              "library - used in a library.",
              "military - used on a military base or similar.",
              "residential - the IP address belongs to a residential ISP or is otherwise primarily used by home users.",
              "router - a backbone or infrastructure router.",
              "school - primary or secondary education.",
              "search_engine_spider - a crawler or indexer for a search engine (Google, Bing, Yahoo, etc.).",
              "traveler - the IP address is used at an airport, hotel, or similar location where the users are generally traveling from their primary residence."
            ]
          }
        }
      },
      "crosscheck_darkweb": {
        "type": "object",
        "properties": {
          "criminalCount": {
            "type": "integer",
            "description": "Count of instances email was observed to have been used in DarkWeb data collections."
          },
          "criminalLastSeen": {
            "type": "string",
            "description": "Last observed time email was observed to have been used in DarkWeb collections."
          },
          "criminalMaxScore": {
            "type": "integer",
            "description": "0-low risk, 5-critical risk.",
            "minimum": 0,
            "maximum": 5
          }
        }
      },
      "crosscheck_confidences": {
        "type": "object",
        "properties": {
          "identity": {
            "type": "number",
            "description": "Overall identity risk confidence. The identity score is a risk score assigned to the user based on their address, email, and phone details. These details are cross-referenced against the data provided by the user or the extracted from their ID.",
            "minimum": 0,
            "maximum": 1
          },
          "activity": {
            "type": [
              "number",
              "null"
            ],
            "description": "Overall activity risk confidence that is based on dynamic attributes."
          }
        }
      },
      "crosscheck_result": {
        "type": "object",
        "description": "CrossCheck Result",
        "properties": {
          "address": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_identity_address"
          },
          "email": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_identity_email"
          },
          "phone": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_identity_phone"
          },
          "gender": {
            "type": "object",
            "$ref": "#/components/schemas/gender_distribution"
          },
          "ageRange": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_age_range"
          },
          "ipAddress": {
            "type": "object",
            "$ref": "#/components/schemas/ip_address"
          },
          "darkWeb": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_darkweb"
          },
          "confidences": {
            "type": "object",
            "$ref": "#/components/schemas/crosscheck_confidences"
          }
        }
      },
      "aamva": {
        "type": "object",
        "properties": {
          "enabled": {
            "type": "boolean",
            "description": "A boolean determining whether or not AAMVA is enabled for the account this job ran under."
          },
          "hasErrors": {
            "type": "boolean",
            "description": "Representing if AAMVA returned any matching errors."
          },
          "hasWarnings": {
            "type": "boolean",
            "description": "Representing if there are any warnings on the AAMVA request."
          },
          "createdAt": {
            "type": "string",
            "description": "Representing when the AAMVA request was created as a [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601)."
          },
          "updatedAt": {
            "type": "string",
            "description": "Representing the last time the AAMVA verification data was updated as a [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601)."
          },
          "status": {
            "type": "string",
            "description": "Representing the state of the AAMVA verification request.",
            "enum": [
              "Pending",
              "In Progress",
              "Error",
              "Not Applicable",
              "Completed"
            ]
          },
          "statusMessage": {
            "type": "string",
            "description": "A message that provides additional information about the status of the verification request."
          },
          "completedAt": {
            "type": "string",
            "description": "Representing the time the verification request was completed as a [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601)."
          }
        }
      },
      "aml_matches": {
        "type": "object",
        "description": "Details of a matched listing for an entity.",
        "properties": {
          "type": {
            "type": "string",
            "description": "The type of list matched."
          },
          "listing_started_utc": {
            "type": "string",
            "description": "The UTC datetime the entity was added to the list."
          },
          "listing_ended_utc": {
            "type": "string",
            "description": "The UTC datetime the entity was removed from the list."
          },
          "name": {
            "type": "string",
            "description": "The name of the list."
          },
          "url": {
            "type": "string",
            "description": "The public URL of the list."
          }
        }
      },
      "aml_hits": {
        "type": "object",
        "description": "Array of hits against submitted term.",
        "properties": {
          "aka": {
            "type": "array",
            "description": "Alternative names for the entity. Note that the \"name\" field is present at the minimum.",
            "items": {
              "type": "string"
            }
          },
          "politicalPositions": {
            "type": "array",
            "description": "An array of potential politcal positions associated with the individual.",
            "items": {
              "type": "string"
            }
          },
          "countries": {
            "type": "array",
            "description": "Associated country names for the entity.",
            "items": {
              "type": "string"
            }
          },
          "matches": {
            "type": "object",
            "description": "List of sanction, warning, and PEP lists the entity matched with.",
            "properties": {
              "sanction": {
                "type": "array",
                "description": "List of sanction lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              },
              "warning": {
                "type": "array",
                "description": "List of warning lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              },
              "pep": {
                "type": "array",
                "description": "List of PEP lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              },
              "pep-class-1": {
                "type": "array",
                "description": "List of PEP Class 1 lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              },
              "pep-class-2": {
                "type": "array",
                "description": "List of PEP Class 2 lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              },
              "pep-class-3": {
                "type": "array",
                "description": "List of PEP Class 3 lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              },
              "pep-class-4": {
                "type": "array",
                "description": "List of PEP Class 4 lists the entity matched with.",
                "items": {
                  "type": "object",
                  "$ref": "#/components/schemas/aml_matches"
                }
              }
            }
          }
        }
      },
      "aml": {
        "type": "object",
        "description": "AML Result",
        "properties": {
          "data": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "description": "Job ID."
              },
              "ref": {
                "type": "string",
                "description": "Numeric search ID."
              },
              "matchStatus": {
                "type": "string",
                "description": "One of 'no_match', 'false_positive', 'potential_match', 'true_positive','unknown'.",
                "enum": [
                  "no_match",
                  "false_positive",
                  "potential_match",
                  "true_positive",
                  "unknown"
                ]
              },
              "riskLevel": {
                "type": "string",
                "description": "One of 'low', 'medium', 'high', 'unknown'.",
                "enum": [
                  "low",
                  "medium",
                  "high",
                  "unknown"
                ]
              },
              "submittedTerm": {
                "type": "string",
                "description": "The name submitted to search against the AML lists."
              },
              "totalHits": {
                "type": "string",
                "description": "The number of entities that matched the submitted term."
              },
              "updatedAt": {
                "type": "string",
                "description": "The date and time the search was last updated (in UTC)."
              },
              "totalMatches": {
                "type": "string",
                "description": "The number of lists that matched the submitted term."
              },
              "hits": {
                "type": "object",
                "$ref": "#/components/schemas/aml_hits"
              }
            }
          },
          "confidence": {
            "type": "object",
            "description": "Confidence score for AML match.",
            "properties": {
              "normalized": {
                "type": "boolean"
              },
              "unnormalized": {
                "type": "boolean"
              }
            }
          }
        }
      },
      "confidences": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number",
            "description": "Confidence score for an id photo.",
            "minimum": 0,
            "maximum": 1
          },
          "idQuality": {
            "type": "number",
            "description": "Confidence score for image quality of the id.",
            "minimum": 0,
            "maximum": 1
          },
          "idGlareQuality": {
            "type": "number",
            "description": "Confidence score for image quality of the id.",
            "minimum": 0,
            "maximum": 1
          },
          "selfie": {
            "type": "number",
            "description": "Confidence score for a selfie photo.",
            "minimum": 0,
            "maximum": 1
          },
          "idMatch": {
            "type": "number",
            "description": "Confidence score for matching data on the id.",
            "minimum": 0,
            "maximum": 1
          },
          "idExpired": {
            "type": "number",
            "description": "Confidence score for id expiration date.",
            "minimum": 0,
            "maximum": 1
          },
          "faceMatch": {
            "type": "number",
            "description": "Confidence score for matching faces.",
            "minimum": 0,
            "maximum": 1
          },
          "birthDateMatch": {
            "type": "number",
            "description": "Confidence score for matching birth dates.",
            "minimum": 0,
            "maximum": 1
          },
          "nameMatch": {
            "type": "number",
            "description": "Confidence score for matching names.",
            "minimum": 0,
            "maximum": 1
          },
          "selfieSunglasses": {
            "type": "number",
            "description": "Confidence score for selfie with sunglasses.",
            "minimum": 0,
            "maximum": 1
          },
          "selfieEyeglasses": {
            "type": "number",
            "description": "Confidence score for selfie with eyeglasses.",
            "minimum": 0,
            "maximum": 1
          }
        }
      },
      "result": {
        "type": "object",
        "properties": {
          "success": {
            "type": "boolean",
            "description": "Did the id verification completed successfully with no errors? The verification could have warnings. Reflects identity verification only; extracted fields such as `height`, `heightCm`, `eyeColor`, and `weight` may be `null` even when `success` is `true`."
          },
          "warnings": {
            "type": "boolean",
            "description": "Does the completed verification contain warnings."
          },
          "gender": {
            "description": "Displays the gender stats for the Job.",
            "type": "object",
            "$ref": "#/components/schemas/gender_info"
          },
          "clientOutput": {
            "description": "Displays information about the theme used, client and the capture type for the images.",
            "type": "object",
            "$ref": "#/components/schemas/client_data"
          },
          "type": {
            "type": "string",
            "description": "The detected [id type](https://docs.vouched.id/docs/recognized-ids). For unrecognized ids, the type will be `other`."
          },
          "state": {
            "type": "string",
            "description": "The issuing state/province/territory of the id as a [ISO 3166-2 code](https://en.wikipedia.org/wiki/ISO_3166-2)."
          },
          "country": {
            "type": "string",
            "description": "The issuing country of the id in [ISO 3166-1 format](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)."
          },
          "id": {
            "type": "string",
            "description": "The verified id number of the id."
          },
          "expireDate": {
            "type": "string",
            "description": "The verified expired date.",
            "pattern": "^\\d{2}\\/\\d{2}\\/\\d{4}$"
          },
          "issueDate": {
            "type": "string",
            "description": "The verified issued date.",
            "pattern": "^\\d{2}\\/\\d{2}\\/\\d{4}$"
          },
          "unverifiedIdAddress": {
            "type": "array",
            "description": "Unverified list of extracted address fields from the ID.",
            "items": {
              "type": "string"
            }
          },
          "idType": {
            "type": "string",
            "description": "Any additional id type information available on the card."
          },
          "ipFraudCheck": {
            "type": "object",
            "description": "Indicator of IP address fraud. The max attempts (default - 4) before a fraud check is triggered and the time range (default - 60 minutes) for the inspection is configurable.",
            "$ref": "#/components/schemas/ipFraudCheck"
          },
          "idAddress": {
            "type": "object",
            "description": "The ID address.",
            "$ref": "#/components/schemas/address"
          },
          "crosscheck": {
            "type": "object",
            "description": "The crosscheck result.",
            "$ref": "#/components/schemas/crosscheck_result"
          },
          "aamva": {
            "type": "object",
            "description": "The aamva result.",
            "$ref": "#/components/schemas/aamva"
          },
          "ipAddress": {
            "type": "object",
            "$ref": "#/components/schemas/ip_address"
          },
          "aml": {
            "type": "object",
            "$ref": "#/components/schemas/aml"
          },
          "class": {
            "type": "string",
            "description": "The ID class value."
          },
          "idFields": {
            "type": "array",
            "description": "Array of objects containing available ID fields.",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Name of available field."
                }
              }
            }
          },
          "endorsements": {
            "type": "string",
            "description": "The id endorsements."
          },
          "motorcycle": {
            "type": "string",
            "description": "The motorcycle property."
          },
          "birthDate": {
            "type": "string",
            "description": "The verified date of birth.",
            "pattern": "^\\d{2}\\/\\d{2}\\/\\d{4}$"
          },
          "firstName": {
            "type": "string",
            "description": "The user's verified first name."
          },
          "middleName": {
            "type": "string",
            "description": "The user's verified middle name."
          },
          "lastName": {
            "type": "string",
            "description": "The user's verified last name."
          },
          "height": {
            "type": [
              "string",
              "null"
            ],
            "description": "The height extracted from the id (for example `5'-10\"` or `6-00`). May be `null` even when `success` is `true` if absent, illegible, or unparseable."
          },
          "heightCm": {
            "type": [
              "number",
              "null"
            ],
            "description": "The extracted height in centimeters. May be `null` even when `success` is `true` (see `height`)."
          },
          "heightInch": {
            "type": [
              "number",
              "null"
            ],
            "description": "The extracted height in inches. May be `null` even when `success` is `true` (see `height`)."
          },
          "eyeColor": {
            "type": [
              "string",
              "null"
            ],
            "description": "The eye color extracted from the id (for example `HAZ`, `BRO`). May be `null` even when `success` is `true` if absent, illegible, or not present on the id."
          },
          "weight": {
            "type": [
              "string",
              "null"
            ],
            "description": "The weight extracted from the id (for example `230`). May be `null` even when `success` is `true` if absent, illegible, or unparseable."
          },
          "weightLb": {
            "type": [
              "number",
              "null"
            ],
            "description": "The extracted weight in pounds. May be `null` even when `success` is `true` (see `weight`)."
          },
          "weightKg": {
            "type": [
              "number",
              "null"
            ],
            "description": "The extracted weight in kilograms. May be `null` even when `success` is `true` (see `weight`)."
          },
          "confidences": {
            "type": "object",
            "description": "Confidence scores with a default threshold of 0.90",
            "$ref": "#/components/schemas/confidences"
          }
        }
      },
      "error": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "description": "\nError type code.\n- InvalidRequestError - The request is invalid.\n\n  - Parameters sent in the request are invalid.\n\n\n- FaceMatchError - The face match score was lower than the threshold.\n\n  - Category: faceMatch\n\n  - Faces obtained from the ID and Selfie images do not match.\n\n\n- NameMatchError - The name match score was lower than the threshold.\n\n  - The name provided by the user and the name extracted from the ID do not match.\n\n  - Eg: User Provided Name - Dave Smith, Extracted Name - David Smith\n\n\n- BarcodeMatchError - The barcode match score was lower than the threshold.\n\n  - The data provided by the user and the data extracted from the barcode do not match. \n\n  - Eg: User Provided Name - Dave Smith, Extracted Name - David Smith\n\n\n- BirthDateMatchError - The birth date match score was lower than the threshold.\n\n  - The birth date provided by the user and the data extracted from the ID do not match.\n\n  - Eg: User Provided DOB - 01/09/1992, Extracted DOB - 09/01/1992\n\n  - Eg: User Provided DOB - 11/09/1992, Extracted DOB - 12/09/1992\n\n\n- ExpiredIdError - The ID’s expiration date has passed.\n\n  - The expiration date extracted from the ID indicates that it has expired.\n\n- InvalidIdPhotoError - The ID is invalid.\n\n  - Category: id\n\n  - The image submitted does not qualify as an ID. The ID image may be of lower quality, have blur, glare or it may be too dark, and hence the data could not be extracted.\n\n- InvalidUserPhotoError - The user photo (selfie) is invalid.\n\n  - Category: selfie\n\n  - The image submitted does not qualify as a selfie.\n\n- AuthenticationError - The request could not be authenticated.\n\n  - The key could not be verified.\n\n- ConnectionError - A connection error occurred while communicating to the Vouched service.\n\n  - UnknownSystemError - A unknown system error occurred.\n\n- TooManyRequestsError - the Vouched service has throttled this request.\n\n  - Retry your request later.\n\n- UnprocessableContentError - The request contains incorrectly formatted or missing data.\n\n  - The server understood the content type of the request content, and the syntax of the request content was correct, but it was unable to process the contained instructions.\n\n  - Eg: Submitted data contains invalid characters\n\n  - Eg: Required data is missing",
            "enum": [
              "InvalidRequestError",
              "FaceMatchError",
              "NameMatchError",
              "BarcodeMatchError",
              "BirthDateMatchError",
              "ExpiredIdError",
              "InvalidIdPhotoError",
              "InvalidUserPhotoError",
              "AuthenticationError",
              "ConnectionError",
              "UnknownSystemError",
              "TooManyRequestsError",
              "UnprocessableContentError"
            ]
          },
          "message": {
            "type": "string",
            "description": "Details on the occurring error."
          },
          "warning": {
            "type": "boolean",
            "description": "Is this a warning?"
          },
          "suggestion": {
            "example": "John Smith",
            "description": "A suggestion for matching name.",
            "type": "string"
          }
        }
      },
      "signals": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "description": "Affected verification category.\n\nid: The id verification category scores indicate the value assigned(`result.confidences.id`) to the uploaded or capture ID image.\n\nselfie: The selfie verification category scores indicate the value assigned(`result.confidences.selfie`) to the uploaded or capture selfie image.\n\nfaceMatch: The faceMatch category score indicates the value assigned(`result.confidences.faceMatch`) to the face match between the ID and selfie images.\n\nbackId: The backId category score indicates the value assigned(`result.confidences.barcode`) to the uploaded or captured back ID image.",
            "enum": [
              "faceMatch",
              "id",
              "selfie",
              "backId"
            ]
          },
          "message": {
            "type": "string",
            "description": "Message associated with the signal."
          },
          "type": {
            "type": "string",
            "description": "Signals affecting the score of the associated verification category. \n\nquality: Indicates the quality/bluriness of the image.\n\nbrightness: Indicates an image with low brightness. \n\nnonglare: Indicates an image with significant glare. \n\nglasses: Selfie image with the user wearing glasses affecting the face match score.\n\nface: Indicator of a face not being found in the image. \n\nfraud: Indicator of visual inconsistencies being found in the image.\n\nbarcode: Indicates a potential error/warning for the barcode scan.\n\nfieldConfidence: Indicates a lower confidence in the extracted values for the field/fields.\n\nmissingName: Indicates the missing field/fields.\n\ndeviceInfo: Provides information about the device used to capture or upload the image.\n\nsticker: Indicates a sticker obscuring the first/last name fields.",
            "enum": [
              "quality",
              "brightness",
              "nonglare",
              "glasses",
              "face",
              "fraud",
              "barcode",
              "fieldConfidence",
              "missingName",
              "deviceInfo",
              "sticker"
            ]
          },
          "fields": {
            "description": "An array of strings of the affected fields.",
            "type": "array"
          },
          "property": {
            "description": "Property of the Signal.",
            "type": "string",
            "enum": [
              "private",
              "public"
            ]
          }
        }
      },
      "response_1": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "The job ID."
          },
          "completed": {
            "type": "boolean",
            "description": "The job is completed."
          },
          "status": {
            "type": "string",
            "description": "The job status",
            "enum": [
              "active",
              "removed",
              "completed"
            ]
          },
          "submitted": {
            "type": "string",
            "example": "2019-09-07T15:50-04:00",
            "description": "The submitted date [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601)."
          },
          "updatedAt": {
            "type": "string",
            "description": "The last updated date [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601).",
            "example": "2019-09-07T15:50-04:00"
          },
          "reviewedAt": {
            "type": "string",
            "description": "The last updated review [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601).",
            "example": "2019-09-07T15:50-04:00"
          },
          "reviewSuccess": {
            "type": "boolean",
            "description": "Review indicates the verification pass or failed."
          },
          "review": {
            "type": "object",
            "description": "Review override object."
          },
          "surveyPoll": {
            "type": "integer",
            "description": "User survey rating.",
            "minimum": 1,
            "maximum": 5
          },
          "surveyMessage": {
            "type": "string",
            "description": "User survey message."
          },
          "surveyAt": {
            "type": "string",
            "description": "The [ISO8601 date](https://en.wikipedia.org/wiki/ISO_8601).",
            "example": "2019-09-07T15:50-04:00"
          },
          "request": {
            "type": "object",
            "description": "Object for 'id-verification'.",
            "$ref": "#/components/schemas/request"
          },
          "result": {
            "type": "object",
            "description": "Object for 'id-verification'.",
            "$ref": "#/components/schemas/result"
          },
          "errors": {
            "type": "array",
            "description": "List of errors for unsuccessful completed jobs.",
            "items": {
              "$ref": "#/components/schemas/error"
            },
            "example": []
          },
          "signals": {
            "type": "array",
            "description": "List of signals affecting id, backId, selfie and faceMatch scores.\n\n\n   | Property | Associated Message |\n   | ----------- |  ----------- |\n   | quality     |   ID/Selfie image is blurry          |\n   | brightness      |  ID/Selfie image is dark          |\n   | nonglare      |   ID/Selfie image has glare           |\n   | glasses      |   Sunglass/Eyeglass worn by user         |\n   | face      |     Required visual markers could not be detected         |\n   | fraud       |  Found visual inconsistencies |\n   | barcode       |  Barcode data does not match extracted data, Barcode process was skipped, Unknown Barcode Error |\n   | fieldConfidence       |  Field/Fields with low confidence: |\n   | missingName       |  Missing Field/Fields: |\n   | deviceInfo       |  Device Info: |\n   | sticker       |  Property/Properties obscured by foreign material: |",
            "items": {
              "$ref": "#/components/schemas/signals"
            }
          },
          "rejectionReasons": {
            "type": "array",
            "description": "List of reasons why the verification was rejected.",
            "items": {
              "type": "object",
              "properties": {
                "key": {
                  "type": "string",
                  "description": "The unique key identifying the rejection reason."
                },
                "description": {
                  "type": "string",
                  "description": "A description of the rejection reason."
                }
              }
            }
          }
        }
      },
      "result_jobs": {
        "type": "object",
        "properties": {
          "items": {
            "type": "array",
            "description": "List of paginated jobs.",
            "items": {
              "$ref": "#/components/schemas/response_1"
            }
          },
          "totalPages": {
            "type": "integer",
            "minimum": 0,
            "description": "Total number of pages of jobs."
          },
          "pageSize": {
            "type": "integer",
            "minimum": 1,
            "description": "The requested page size."
          },
          "page": {
            "type": "integer",
            "minimum": 1,
            "description": "The requested page."
          },
          "total": {
            "type": "integer",
            "minimum": 0,
            "description": "Total number of filtered jobs."
          }
        }
      },
      "errors": {
        "type": "object",
        "description": "List of errors for unsuccessful completed jobs.",
        "properties": {
          "errors": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/error"
            }
          }
        }
      }
    },
    "responses": {
      "400": {
        "description": "InvalidRequestError - The request is invalid.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "InvalidRequestError",
                  "message": "Invalid request"
                }
              ]
            }
          }
        }
      },
      "401": {
        "description": "AuthenticationError - The request could not be authenticated.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "AuthenticationError",
                  "message": "Unauthorized access"
                }
              ]
            }
          }
        }
      },
      "404": {
        "description": "ConnectionError - A connection error occurred while communicating to the Vouched service.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "ConnectionError",
                  "message": "Connection error"
                }
              ]
            }
          }
        }
      },
      "429": {
        "description": "TooManyRequestsError - the Vouched service has throttled this request.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "TooManyRequestsError",
                  "message": "Too many requests error"
                }
              ]
            }
          }
        }
      },
      "500": {
        "description": "UnknownSystemError - A unknown system error occurred.",
        "content": {
          "application/json; charset=utf-8": {
            "schema": {
              "$ref": "#/components/schemas/errors"
            },
            "example": {
              "errors": [
                {
                  "type": "UnknownSystemError",
                  "message": "Oops, we encountered a problem"
                }
              ]
            }
          }
        }
      }
    }
  },
  "x-tagGroups": [
    {
      "name": "APIs",
      "tags": [
        "jobs",
        "invites",
        "crosscheck",
        "aml",
        "ssn",
        "tin",
        "dob",
        "documents"
      ]
    }
  ]
}
```