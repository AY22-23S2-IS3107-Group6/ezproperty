import { Box, Button, Input, SimpleGrid } from "@chakra-ui/react";
import { Field, Formik, useFormik } from "formik";
import {
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
} from "@chakra-ui/react"

const Form = (props) => {
  const initialValues = {
    street: "",
    district: 1,
    propertyType: "",
    area: 0,
    price: 0,
    transactionDate: new Date(),
    tenure: 0,
    resale: ""
  }

  // const onSubmit = values => {
  //   console.log("Form data", values)
  // }

  function validateStreet(value) {
    let error
    if (!value) {
      error = "Street is required"
    }
    return error
  }

  // difference btw 0 and empty field
  function validateDistrict(value) {
    let error
    if (value < 1) {
      error = "District must be larger than 0"
    } else if (value > 28) {
      error = "Singapore only has 28 districts"
    } else if (value == null) {
      error = "District is required"
    }
    return error
  }

  function validatePropertyType(value) {
    let error
    if (!value) {
      error = "Property type is required"
    }
    return error
  }

  function validateArea(value) {
    let error
    if (value < 1) {
      error = "Area must be larger than 0"
    } else if (!value) {
      error = "Area is required"
    }
    return error
  }

  function validatePrice(value) {
    let error
    if (value < 1) {
      error = "Price must be higher than $0"
    } else if (!value) {
      error = "Price is required"
    }
    return error
  }

  function validateTransactionDate(value) {
    let error
    if (!value) {
      error = "Transaction date is required"
    }
    return error
  }

  function validateTenure(value) {
    let error
    if (value < 1) {
      error = "Property must have tenure left"
    } else if (!value) {
      error = "Tenure is required"
    }
    return error
  }

  function validateResale(value) {
    let error
    if (!value) {
      error = "Required"
    } else if (value.toLowerCase() !== "resale" && value.toLowerCase() !== "private") {
      error = "Has to be either resale or private"
    }
    return error
  }

  // const formik = useFormik({
  //   initialValues,
  //   onSubmit,
  //   validate
  // })

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <SimpleGrid
        columns={{ base: 1, md: 2, lg: 3, "2xl": 6 }}
        gap="20px"
        mb="20px">
        <Formik
          initialValues={initialValues}
          onSubmit={(values, actions) => {
            setTimeout(() => {
              alert(JSON.stringify(values, null, 2))
              actions.setSubmitting(false)
            }, 1000)
          }}
        >
          {(props) => (
            <form>
              <Field name="street" validate={validateStreet}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.street && form.touched.street}>
                    <FormLabel htmlFor="street">Street</FormLabel>
                    <Input
                      {...field}
                      id="street"
                      placeholder="Street Name"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.street}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="district" validate={validateDistrict}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.district && form.touched.district}>
                    <FormLabel htmlFor="district">District Number</FormLabel>
                    <Input
                      {...field}
                      id="district"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.district}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="propertyType" validate={validatePropertyType}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.propertyType && form.touched.propertyType}>
                    <FormLabel htmlFor="propertyType">Property Type</FormLabel>
                    <Input
                      {...field}
                      id="Property Type"
                      placeholder="Property Type"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.propertyType}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="area" validate={validateArea}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.area && form.touched.area}>
                    <FormLabel htmlFor="area">Area (in square metre)</FormLabel>
                    <Input
                      {...field}
                      id="area"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.area}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="price" validate={validatePrice}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.price && form.touched.price}>
                    <FormLabel htmlFor="price">Price</FormLabel>
                    <Input
                      {...field}
                      id="price"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.price}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="transactionDate" validate={validateTransactionDate}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.transactionDate && form.touched.transactionDate}>
                    <FormLabel htmlFor="transactionDate">Transaction Date</FormLabel>
                    <Input
                      {...field}
                      id="transactionDate"
                      type="date"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.transactionDate}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="tenure" validate={validateTenure}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.tenure && form.touched.tenure}>
                    <FormLabel htmlFor="tenure">Tenure</FormLabel>
                    <Input
                      {...field}
                      id="tenure"
                      type="number"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.tenure}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

              <Field name="resale" validate={validateResale}>
                {({ field, form }) => (
                  <FormControl isInvalid={form.errors.resale && form.touched.resale}>
                    <FormLabel htmlFor="resale">Resale</FormLabel>
                    <Input
                      {...field}
                      id="resale"
                      placeholder="Resale / Private"
                      borderRadius="16px"
                    />
                    <FormErrorMessage>{form.errors.resale}</FormErrorMessage>
                  </FormControl>
                )}
              </Field>

      

              <Button type="submit">Submit</Button>
            </form>
          )}

        </Formik>

      </SimpleGrid>
    </Box>


    // <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
    //   <SimpleGrid
    //     columns={{ base: 1, md: 2, lg: 3, "2xl": 6 }}
    //     gap="20px"
    //     mb="20px"
    //   >
    //     <Formik
    //       initialValues={{ name: "Sasuke" }}
    //       // onSubmit={(values, actions) => {
    //       //   setTimeout(() => {
    //       //     alert(JSON.stringify(values, null, 2))
    //       //     actions.setSubmitting(false)
    //       //   }, 1000)
    //       // }}
    //     >
    //       {(props) => (
    //         <form>
    //           <Field name="name" validate={validateStreet}>
    //             {({ field, form }) => (
    //               <FormControl isInvalid={form.errors.name && form.touched.name}>
    //                 <FormLabel htmlFor="name">First name</FormLabel>
    //                 <Input
    //                   {...field}
    //                   id="name"
    //                   placeholder="name"
    //                   borderRadius="16px"
    //                 />
    //                 <FormErrorMessage>{form.errors.name}</FormErrorMessage>
    //               </FormControl>
    //             )}
    //           </Field>

    //           <Field name="name" validate={validateStreet}>
    //             {({ field, form }) => (
    //               <FormControl isInvalid={form.errors.name && form.touched.name}>
    //                 <FormLabel htmlFor="name">First name</FormLabel>
    //                 <Input
    //                   {...field}
    //                   id="name"
    //                   placeholder="name"
    //                   borderRadius="16px"
    //                 />
    //                 <FormErrorMessage>{form.errors.name}</FormErrorMessage>
    //               </FormControl>
    //             )}
    //           </Field>

    //           <Button
    //             mt={4}
    //             colorScheme="brand"
    //             isLoading={props.isSubmitting}
    //             type="submit"
    //           >
    //             Submit
    //           </Button>
    //         </form>
    //       )}
    //     </Formik>
    //   </SimpleGrid>
    // </Box>




  );
};

export default Form;
