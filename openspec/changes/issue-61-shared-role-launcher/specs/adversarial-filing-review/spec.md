# adversarial-filing-review Delta

## MODIFIED Requirements

### Requirement: Stateless trusted provider runtime

The public adversarial reviewer SHALL execute through the shared protected
static-role launcher. Its role definition MUST preserve the existing stateless
no-tools OpenAI request, five-category output validator, independence,
read-only-target, and plaintiff-decision boundaries. Provider and profile data
MUST NOT add tools, storage, conversation identifiers, filesystem paths,
target-mutation authority, or automatic remediation.

#### Scenario: Trusted review is dispatched

- **WHEN** its role, profile, filing target, approved context, model credential,
  explicit output folder, and isolation adapter validate
- **THEN** one fresh shared-launcher execution returns only the validated
  advisory review for trusted-host publication
