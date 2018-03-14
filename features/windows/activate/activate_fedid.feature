Feature: Windows client FedID activate

  Background:
    When Windows Client is not activated


  @smoke @KAL-012 @gui @fedid-activate
  Scenario: Windows FedID activate from GUI

    When I open Login window
    When I fedid activate windows gui with
      | email                               | password  | product_key          | encryption_type | encryption_key | oem            | env  | subdomain      | rely_trust           |
      | zoeadminreauth2@mtdev.mozypro.local | abc!@#123 | QEZA74E9V3RGZ3WT27SQ | pkey            | test1234       | MozyEnterprise | QA12 | fedidpush      | fedidpush_qa6        |
      | qa12nonoempush2@mtdev.mozypro.local | abc!@#123 | 6SQD6S23TXS2SW332ZVA | pkey            | test1234       | mozypro        | QA12 | qa12nonoempull | Trust.qa12nonoempull |
