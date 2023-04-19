import { Field, Formik, Form } from "formik";
import * as Yup from "yup"
import {
    Box,
    Button,
    FormControl,
    FormLabel,
    FormErrorMessage,
    Input,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    SimpleGrid,
    useDisclosure
} from "@chakra-ui/react"

import axios from "axios";
import { useEffect, useState } from "react";

const PredictivePriceForm = (props) => {
    const initialValues = {
        street: "",
        floor: 0,
        district: 1,
        area: 0,
        transactionDate: new Date(),
        resale: ""
    }
    const [predictedPrice, setPredictedPrice] = useState(null);
    const { isOpen, onOpen, onClose } = useDisclosure()

    const onSubmit = async (values) => {
        const params = {
            "floor": values.floor,
            "district": values.district,
            "area": values.area,
            "transactionDate": values.transactionDate,
            "resale": values.resale
        }

        try {
            axios.get('http://localhost:5000/predictpropertyprice', {
                params: params
            })
                .then((response) => response.data)
                .then((json) => {
                    if (typeof json === "number") {
                        json = JSON.parse(json);
                        console.log(json)
                    }
                    setPredictedPrice(json);
                    onOpen();
                })
                .catch((err) => console.log(err));
        } catch (error) {
            console.error("Error:", error);
        }
    }

    // useEffect(() => {
    //     onOpen();
    // }, [predictedPrice]);

    const validationSchema = Yup.object({
        street: Yup.string().required("Street is required!"),
        floor: Yup.number()
            .min(0, "Floor level cannot be negative")
            .required("Floor level is required!"),
        district: Yup.number()
            .min(1, "District must be larger than 0")
            .max(28, "Singapore only has 28 districts")
            .required("District is required!"),
        area: Yup.number()
            .positive("Area must be positive")
            .required("Area is required!"),
        transactionDate: Yup.date()
            .min(new Date(), "Property should not be sold yet"),
        resale: Yup.mixed()
            .oneOf(["private", "resale"], "Has to be either resale or private")
            .required("Resale/ Private is required!"),
    })

    return (
        <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
            <SimpleGrid
                columns={{ base: 1, md: 2, lg: 3, "2xl": 6 }}
                gap="20px"
                mb="20px">
                <Formik
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                    onSubmit={onSubmit}
                >
                    {(props) => (
                        <Form action='http://localhost:5000/predictpropertyprice' method="get">
                            <Field name="street">
                                {({ field, form }) => (
                                    <FormControl isInvalid={form.errors.street && form.touched.street}>
                                        <FormLabel htmlFor="street">Street Name</FormLabel>
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

                            <Field name="floor">
                                {({ field, form }) => (
                                    <FormControl isInvalid={form.errors.floor && form.touched.floor}>
                                        <FormLabel htmlFor="floor">Floor Level</FormLabel>
                                        <Input
                                            {...field}
                                            id="floor"
                                            type="number"
                                            borderRadius="16px"
                                        />
                                        <FormErrorMessage>{form.errors.floor}</FormErrorMessage>
                                    </FormControl>
                                )}
                            </Field>

                            <Field name="district">
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

                            <Field name="area">
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

                            <Field name="transactionDate">
                                {({ field, form }) => (
                                    <FormControl isInvalid={form.errors.transactionDate && form.touched.transactionDate}>
                                        <FormLabel htmlFor="transactionDate">Future Transaction Date</FormLabel>
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

                            <Field name="resale">
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

                            <Button
                                mt={4}
                                colorScheme="brand"
                                // isLoading={props.isSubmitting}
                                type="submit">
                                Submit
                            </Button>
                        </Form>
                    )}

                </Formik>

                <>
                    <Modal isOpen={isOpen} onClose={onClose}>
                        <ModalOverlay />
                        <ModalContent>
                            <ModalHeader>Predicted Property Price</ModalHeader>
                            <ModalCloseButton />
                            <ModalBody>
                                <div>
                                    {predictedPrice}
                                </div>
                            </ModalBody>
                            <ModalFooter>
                                <Button colorScheme="brand" mr={3} onClick={onClose}>
                                    Close
                                </Button>
                            </ModalFooter>
                        </ModalContent>
                    </Modal>
                </>
            </SimpleGrid>
        </Box>
    );
};

export default PredictivePriceForm;
