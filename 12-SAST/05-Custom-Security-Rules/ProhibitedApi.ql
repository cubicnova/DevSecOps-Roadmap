/**
 * @name Review calls to a prohibited API
 * @description Flags calls to an API that requires security review.
 * @kind problem
 * @id py/prohibited-api-review
 * @problem.severity warning
 * @security-severity 5.0
 * @precision medium
 * @tags security
 */

import python

from Call call
where call.getFunc().toString() = "legacy_request"
select call, "Review this call and use the approved secure client."
